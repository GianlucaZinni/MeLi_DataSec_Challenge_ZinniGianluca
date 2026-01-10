# Mercado Libre DataSec Challenge

Este repositorio contiene las soluciones del desafío técnico.

## Entorno
- `Python 3.12.10`
- `Go (versión especificada en el archivo de la solución)`

## Estructura
Cada desafío se implementa en un archivo separado, utilizando el nombre de archivo exacto especificado en las instrucciones:
- `solution_minesweeper.py`
- `solution_best_in_genre.py`
- `applicant_query.sql`
- `solution_summarizer.go`

## Pruebas locales
- Posicionate en la raiz del repo: `cd meli_challenge`.
- Ejecuta todos los tests de Python (mock): `python -m unittest -v`
- Minesweeper: `python -m unittest -v test_solution_minesweeper.py`
- Best in Genre: `python test_solution_best_in_genre.py --mock` (usa `--all` para incluir live contra la API)
- SQL (applicant_query): `python -m unittest -v test_solution_applicant_query.py` (usa sqlite3 en memoria)
- Go (summarizer): `go test ./...` y ejemplo de uso `go run solution_summarizer.go --input archivo.txt --type bullet` (Go 1.25.5)
- Los tests de Python usan solo la biblioteca estandar de Python 3.12.10, sin dependencias externas.

## Contacto

- **Nombre:** Gianluca Zinni
- **Email:** zinnigianluca@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/gianlucazinni/
