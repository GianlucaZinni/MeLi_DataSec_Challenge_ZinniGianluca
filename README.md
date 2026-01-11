# Mercado Libre DataSec Challenge

Este repositorio contiene las soluciones del desafío técnico.

## Entorno
- Python 3.12.10
- Go 1.25.5 (para el summarizer)

## Instrucciones del challenge
- Documento base del reto: [DataSec_Challenge_EN_v3.md](DataSec_Challenge_EN_v3.md)

## Estructura
```
.
├─ README.md
├─ DataSec_Challenge_EN_v3.md
├─ .gitignore
├─ .envexample
├─ challenges/
│  ├─ solution_minesweeper.py
│  ├─ solution_best_in_genre.py
│  ├─ applicant_query.sql
│  └─ summarizer/
│     ├─ solution_summarizer.go
│     ├─ solution_summarizer_test.go
│     ├─ go.mod
│     ├─ sample.txt
│     └─ summarizer_execution_log.txt
├─ docs/
│  ├─ minesweeper.md
│  ├─ best_in_genre.md
│  ├─ applicant_query.md
│  └─ summarizer.md
└─ tests/
   ├─ test_solution_minesweeper.py
   ├─ test_solution_best_in_genre.py
   └─ test_solution_applicant_query.py
```

## Enlaces rápidos:
- Docs: [Minesweeper](docs/minesweeper.md) · [Best in Genre](docs/best_in_genre.md) · [SQL Failures](docs/applicant_query.md) · [Summarizer](docs/summarizer.md)
- Código: [Minesweeper](challenges/solution_minesweeper.py) · [Best in Genre](challenges/solution_best_in_genre.py) · [SQL](challenges/applicant_query/applicant_query.sql) · [Summarizer](challenges/summarizer/solution_summarizer.go)
- Tests: [Py Minesweeper](tests/test_solution_minesweeper.py) · [Py Best in Genre](tests/test_solution_best_in_genre.py) · [Py SQL](tests/test_solution_applicant_query.py) · [Go Summarizer](challenges/summarizer/solution_summarizer_test.go)

## Pruebas locales (por challenge)
- **Minesweeper**  
  - Código: `challenges/solution_minesweeper.py`  
  - Docs: `docs/minesweeper.md`  
  - Test: `python tests/test_solution_minesweeper.py`

- **Best in Genre**  
  - Código: `challenges/solution_best_in_genre.py`  
  - Docs: `docs/best_in_genre.md`  
  - Tests: `python tests/test_solution_best_in_genre.py` + `--mock` o `--live` (usa `--all` para incluir todos)

- **SQL: Advertising Failures**  
  - SQL: `challenges/applicant_query/applicant_query.sql`  
  - Docs: `docs/applicant_query.md`  
  - Test: `python tests/test_solution_applicant_query.py`

- **Go Summarizer**  
  - Código: `challenges/summarizer/solution_summarizer.go`  
  - Docs: `docs/summarizer.md` y `docs/go_summarizer.md`  
  - Tests (en `challenges/summarizer`): `go test`  
  - Ejemplo: `go run solution_summarizer.go --input sample.txt --type bullet` (requiere `HUGGINGFACE_TOKEN`; lee `.env` si existe)

## Contacto
- Nombre: Gianluca Zinni
- Email: zinnigianluca@gmail.com
- LinkedIn: https://www.linkedin.com/in/gianlucazinni/
