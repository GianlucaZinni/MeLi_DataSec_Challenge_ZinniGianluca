// Tests for solution_summarizer.go using Go 1.25.5
package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
)

func TestBuildPromptVariants(t *testing.T) {
	text := "Example text."
	if got := buildPrompt("short", text); !strings.Contains(got, "1-2 sentence") {
		t.Fatalf("short prompt missing hint: %q", got)
	}
	if got := buildPrompt("medium", text); !strings.Contains(got, "one-paragraph") {
		t.Fatalf("medium prompt missing hint: %q", got)
	}
	if got := buildPrompt("bullet", text); !strings.Contains(got, "bullet list") {
		t.Fatalf("bullet prompt missing hint: %q", got)
	}
}

func TestFetchSummaryWithMockServer(t *testing.T) {
	t.Setenv("HUGGINGFACE_TOKEN", "dummy")
	mock := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var body map[string]string
		_ = json.NewDecoder(r.Body).Decode(&body)
		// Echo back a generated_text field to simulate the HF response shape.
		resp := []map[string]string{{"generated_text": "summary: " + body["inputs"][:7]}}
		_ = json.NewEncoder(w).Encode(resp)
	}))
	defer mock.Close()

	origEndpoint := defaultModelEndpoint
	defaultModelEndpoint = mock.URL
	defer func() { defaultModelEndpoint = origEndpoint }()

	summary, err := fetchSummary("short", "abcdefg...")
	if err != nil {
		t.Fatalf("fetchSummary returned error: %v", err)
	}
	if !strings.HasPrefix(summary, "summary:") {
		t.Fatalf("unexpected summary: %q", summary)
	}
}

func TestParseArgsMissingInput(t *testing.T) {
	os.Args = []string{"cmd"}
	if _, _, err := parseArgs(); err == nil {
		t.Fatal("expected error when input is missing")
	}
}

func TestFetchSummaryRequiresToken(t *testing.T) {
	t.Setenv("HUGGINGFACE_TOKEN", "")
	if _, err := fetchSummary("short", "text"); err == nil {
		t.Fatalf("expected error when token missing")
	}
}

func TestFormatSummaryBulletizes(t *testing.T) {
	raw := "Sentence one. Sentence two! Sentence three?"
	got := formatSummary("bullet", raw)
	lines := strings.Split(got, "\n")
	if len(lines) != 3 {
		t.Fatalf("expected 3 bullets, got %d: %v", len(lines), lines)
	}
	for _, ln := range lines {
		if !strings.HasPrefix(ln, "- ") {
			t.Fatalf("line not bullet-prefixed: %q", ln)
		}
	}
}

func TestFormatSummaryShortTrimsSentences(t *testing.T) {
	raw := "First sentence. Second sentence. Third sentence without stop"
	got := formatSummary("short", raw)
	if strings.Contains(got, "Third sentence") {
		t.Fatalf("short summary should limit to two sentences, got: %q", got)
	}
}
