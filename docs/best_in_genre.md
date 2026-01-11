# REST API: Best TV Shows in Genre (Python 3.12.10)

[Volver al README](../README.md)

Referencia: `challenges/solution_best_in_genre.py`

## Objetivo
Obtener el nombre de la serie con mayor `imdb_rating` para un género dado, usando la API paginada `https://jsonmock.hackerrank.com/api/tvseries?page={num}`. Empates se resuelven por orden alfabético del nombre (A-Z).

## Paso a paso del código
1) **Validación de entrada**
   - Si `genre` no es `str` o es vacío tras `strip()`, se devuelve `""` para evitar llamadas innecesarias.
2) **Normalización del género**
   - `target_genre = genre.strip().lower()` para comparar en minúsculas sin espacios extra.
3) **Inicialización**
   - `base_url` fija el endpoint paginado.
   - `page = 1` y `total_pages = None` controlan la paginación.
   - `best_name = ""`, `best_rating = -inf` guardan el mejor candidato.
4) **Bucle de paginación**
   - Llama `urllib.request.urlopen(base_url + page)`, decodifica JSON; en errores de red/parseo, retorna `""`.
   - En la primera iteración toma `total_pages` para saber cuándo detenerse.
5) **Procesamiento de cada serie**
   - Divide `genre` por comas (`entry.strip().lower()`), compara con `target_genre`.
   - Toma `name` y `imdb_rating`, los valida y convierte rating a `float`.
   - Actualiza mejor candidato si el rating es mayor o, en empate, si el nombre es alfabéticamente menor.
6) **Avance de página**
   - `page += 1` hasta `page > total_pages`.
7) **Retorno**
   - Devuelve `best_name`; si nada califica o hay error, retorna `""`.

## Consideraciones de diseño
- Solo biblioteca estándar (`urllib.request`, `json`).
- Manejo defensivo de errores devolviendo `""`.
- Coincidencia de género insensible a mayúsculas/minúsculas.
- Paginación completa usando `total_pages`.

## Cómo probar
1) Instalar Python 3.12.10.
2) Ejecutar pruebas desde la raíz:
   - Solo mocks (sin red):
     ```bash
     python tests/test_solution_best_in_genre.py --mock
     ```
   - Solo live contra la API real:
     ```bash
     python tests/test_solution_best_in_genre.py --live
     ```
   - Todas (mocks + live):
     ```bash
     python tests/test_solution_best_in_genre.py --all
     ```
   Las pruebas live usan la red y pueden tardar más.
