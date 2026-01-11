// Go 1.25.5
// CLI: summarize a text file via a public GenAI API (Hugging Face Inference).
//
// Design:
//   - Standard library only (net/http, encoding/json, flag, os).
//   - Accepts --input (or positional) for the file path and --type/-t for summary style: short|medium|bullet.
//   - Builds an instruction prompt tailored to the requested type and sends it to the Hugging Face Inference API
//     (facebook/bart-large-cnn summarization). Docs: https://huggingface.co/docs/api-inference/index
//   - If HUGGINGFACE_TOKEN is set, it is passed as Bearer; otherwise it attempts an unauthenticated request
//     (may be rate-limited). Errors are reported to stderr with a non-zero exit code.
package main

import (
	"bytes"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"
)

// Updated per Hugging Face notice: router.huggingface.co replaces api-inference.huggingface.co
var defaultModelEndpoint = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

type hfResponse struct {
	SummaryText   string `json:"summary_text"`
	GeneratedText string `json:"generated_text"`
}

func main() {
	loadDotEnv()
	inputPath, summaryType, err := parseArgs()
	if err != nil {
		fmt.Fprintln(os.Stderr, "Argument error:", err)
		os.Exit(1)
	}

	content, err := os.ReadFile(inputPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to read input file:", err)
		os.Exit(1)
	}

	prompt := buildPrompt(summaryType, string(content))
	summary, err := fetchSummary(summaryType, prompt)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Failed to get summary:", err)
		os.Exit(1)
	}

	fmt.Println(formatSummary(summaryType, summary))
}

func parseArgs() (string, string, error) {
	input := flag.String("input", "", "Path to the text file to summarize (positional also accepted)")
	sType := flag.String("type", "short", "Summary type: short|medium|bullet")
	flag.StringVar(sType, "t", "short", "Summary type: short|medium|bullet (shorthand)")
	flag.Parse()

	if *input == "" && flag.NArg() > 0 {
		*input = flag.Arg(0)
	}
	if *input == "" {
		return "", "", errors.New("missing --input <file> (or positional file path)")
	}

	summaryType := strings.ToLower(strings.TrimSpace(*sType))
	if summaryType != "short" && summaryType != "medium" && summaryType != "bullet" {
		return "", "", fmt.Errorf("invalid --type %q (use short|medium|bullet)", summaryType)
	}
	return *input, summaryType, nil
}

func buildPrompt(summaryType, text string) string {
	base := strings.TrimSpace(text)
	switch summaryType {
	case "short":
		return "Provide ONLY a concise 1-2 sentence summary of the following text.\n\n" + base
	case "medium":
		return "Provide ONLY a one-paragraph summary of the following text.\n\n" + base
	case "bullet":
		return "Provide ONLY a concise bullet list summary of the following text. Use '- ' to prefix each bullet and one bullet per line.\n\n" + base
	default:
		return base
	}
}

func fetchSummary(summaryType, prompt string) (string, error) {
	payload := map[string]any{
		"inputs":     prompt,
		"parameters": map[string]any{"max_new_tokens": maxTokensFor(summaryType)},
	}
	body, err := json.Marshal(payload)
	if err != nil {
		return "", err
	}

	token := os.Getenv("HUGGINGFACE_TOKEN")
	if token == "" {
		return "", errors.New("missing HUGGINGFACE_TOKEN (required by router.huggingface.co)")
	}

	req, err := http.NewRequest("POST", defaultModelEndpoint, bytes.NewReader(body))
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+token)

	client := &http.Client{Timeout: 25 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		slurp, _ := io.ReadAll(io.LimitReader(resp.Body, 1024))
		return "", fmt.Errorf("API error: status %d body: %s", resp.StatusCode, strings.TrimSpace(string(slurp)))
	}

	var parsed []hfResponse
	if err := json.NewDecoder(resp.Body).Decode(&parsed); err != nil {
		return "", fmt.Errorf("failed to decode response: %w", err)
	}
	if len(parsed) == 0 {
		return "", errors.New("empty response from API")
	}

	if parsed[0].SummaryText != "" {
		return strings.TrimSpace(parsed[0].SummaryText), nil
	}
	if parsed[0].GeneratedText != "" {
		return strings.TrimSpace(parsed[0].GeneratedText), nil
	}
	return "", errors.New("no summary text in response")
}

// formatSummary post-processes the raw summary for better bullet formatting when needed.
func formatSummary(summaryType, summary string) string {
	summary = strings.TrimSpace(summary)
	switch summaryType {
	case "bullet":
		lines := strings.Split(summary, "\n")
		hasBullets := false
		for _, ln := range lines {
			if strings.HasPrefix(strings.TrimSpace(ln), "- ") {
				hasBullets = true
				break
			}
		}
		if hasBullets {
			return strings.Join(lines, "\n")
		}
		// Split into sentences and prefix with "- ".
		split := sentenceSplit(summary)
		var bullets []string
		for _, s := range split {
			s = strings.TrimSpace(s)
			if s == "" {
				continue
			}
			bullets = append(bullets, "- "+s)
		}
		if len(bullets) == 0 {
			return summary
		}
		return strings.Join(bullets, "\n")
	case "short":
		sentences := sentenceSplit(summary)
		if len(sentences) == 0 {
			return summary
		}
		if len(sentences) > 2 {
			sentences = sentences[:2]
		}
		return strings.TrimSpace(strings.Join(sentences, " "))
	case "medium":
		sentences := sentenceSplit(summary)
		if len(sentences) == 0 {
			return summary
		}
		if len(sentences) > 4 {
			sentences = sentences[:4]
		}
		return strings.TrimSpace(strings.Join(sentences, " "))
	default:
		return summary
	}
}

// sentenceSplit is a simple splitter on ., !, ? keeping basic bulletization.
func sentenceSplit(text string) []string {
	separators := []rune{'.', '!', '?'}
	var parts []string
	var buf strings.Builder
	for _, r := range text {
		buf.WriteRune(r)
		if containsRune(separators, r) {
			parts = append(parts, buf.String())
			buf.Reset()
		}
	}
	if buf.Len() > 0 {
		parts = append(parts, buf.String())
	}
	return parts
}

func containsRune(set []rune, r rune) bool {
	for _, s := range set {
		if s == r {
			return true
		}
	}
	return false
}

func maxTokensFor(summaryType string) int {
	switch summaryType {
	case "short":
		return 60
	case "medium":
		return 160
	case "bullet":
		return 200
	default:
		return 120
	}
}

// loadDotEnv loads environment variables from a .env file if present (KEY=VALUE per line, # for comments).
func loadDotEnv() {
	paths := []string{
		".env",
		".." + string(os.PathSeparator) + ".env",
		".." + string(os.PathSeparator) + ".." + string(os.PathSeparator) + ".env",
	}
	for _, p := range paths {
		content, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		lines := strings.Split(string(content), "\n")
		for _, line := range lines {
			line = strings.TrimSpace(line)
			if line == "" || strings.HasPrefix(line, "#") {
				continue
			}
			parts := strings.SplitN(line, "=", 2)
			if len(parts) != 2 {
				continue
			}
			key := strings.TrimSpace(parts[0])
			val := strings.TrimSpace(parts[1])
			if key != "" {
				_ = os.Setenv(key, val)
			}
		}
	}
}
