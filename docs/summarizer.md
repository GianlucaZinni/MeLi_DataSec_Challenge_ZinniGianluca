# Go CLI: Text Summarizer with GenAI (Go 1.25.5)

[Volver al README](../README.md)

Referencia: `challenges/summarizer/solution_summarizer.go`

## Objetivo
CLI en Go que lee un archivo de texto y genera un resumen usando el router de Hugging Face (`facebook/bart-large-cnn`). Soporta tipos de resumen: `short`, `medium`, `bullet`. Requiere `HUGGINGFACE_TOKEN` (el programa carga `.env` automáticamente si existe).

## Uso
```bash
# desde challenges/summarizer
# resumen corto (1-2 oraciones)
go run solution_summarizer.go --input ruta/al/archivo.txt --type short

# resumen medio (un párrafo)
go run solution_summarizer.go -t medium ruta/al/archivo.txt

# resumen en viñetas
go run solution_summarizer.go --input archivo.txt --type bullet
```
- Antes de ejecutar define el token (opciones):
  - Crear un `.env` copiando `.envexample` y completar `HUGGINGFACE_TOKEN=<tu_token>`.
  - O bien:
    - PowerShell: `$env:HUGGINGFACE_TOKEN="<tu_token>"`
    - Bash: `export HUGGINGFACE_TOKEN="<tu_token>"`
  - Cómo obtenerlo: crea/usa una cuenta gratuita en https://huggingface.co/settings/tokens, confirma tu correo y genera un Access Token (scope "read"). Copia ese token en la variable.

## Recorrido del código
1) **Parseo de argumentos** (`parseArgs`):
   - Flags `--input` (o posicional) y `--type/-t` (`short|medium|bullet`).
   - Valida que exista la ruta y que el tipo sea válido.
2) **Lectura de archivo**:
   - `os.ReadFile` carga el texto a resumir.
3) **Construcción del prompt** (`buildPrompt`):
   - Ajusta el tono según el tipo:
     - short: 1-2 oraciones.
     - medium: un párrafo.
     - bullet: lista con prefijo `- `.
4) **Llamada a la API** (`fetchSummary`):
   - Endpoint: `https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn`.
   - Body JSON: `{"inputs": "<prompt>", "parameters": {"max_new_tokens": <según tipo>}}` con topes por tipo (`short` más corto, `medium` intermedio, `bullet` más amplio).
   - Header `Authorization: Bearer <HUGGINGFACE_TOKEN>` (requerido). Si `.env` existe, se carga antes de leer la variable.
   - Timeout de 25s; maneja errores HTTP y decodifica JSON buscando `summary_text` o `generated_text`.
5) **Salida**:
   - Imprime el resumen a stdout; errores a stderr con salida distinta de cero.
   - Postprocesado: `bullet` genera viñetas si no vienen ya; `short` limita a 2 oraciones y `medium` a 4, para evitar cortes abruptos.

## Pruebas
- Unit tests (sin llamadas reales, usando `httptest`):
  ```bash
  go test
  ```
  Cobertura:
  - `buildPrompt` para los tres tipos.
  - `fetchSummary` contra un servidor HTTP simulado.
  - `parseArgs` lanza error si falta `--input`.
  - `formatSummary` convierte texto plano en viñetas cuando es necesario.

## Notas
- Solo biblioteca estándar de Go.
- Versión documentada en cabecera: Go 1.25.5.
- El router de Hugging Face exige `HUGGINGFACE_TOKEN`; sin token la solicitud fallará.
