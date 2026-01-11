# SQL: Advertising System Failures Report (SQL + Python 3.12.10)

[Volver al README](../README.md)

Referencia: `challenges/applicant_query/applicant_query.sql`

## Objetivo
Listar los clientes que tienen más de 3 eventos con `status = 'failure'`, mostrando su nombre completo y el recuento de fallos, ordenados de mayor a menor.

## Paso a paso del SQL
```sql
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    COUNT(*) AS failures
FROM customers AS c
JOIN campaigns AS cp
    ON cp.customer_id = c.id
JOIN events AS e
    ON e.campaign_id = cp.id
WHERE e.status = 'failure'
GROUP BY c.first_name, c.last_name
HAVING COUNT(*) > 3
ORDER BY failures DESC;
```
- `CONCAT(c.first_name, ' ', c.last_name)`: arma el nombre completo como `customer`.
- `COUNT(*) AS failures`: cuenta los eventos filtrados como fallos.
- `JOIN` entre `customers` → `campaigns` → `events` para vincular eventos con sus clientes.
- `WHERE e.status = 'failure'`: solo eventos fallidos.
- `GROUP BY c.first_name, c.last_name`: agrupa por cliente.
- `HAVING COUNT(*) > 3`: solo clientes con más de 3 fallos.
- `ORDER BY failures DESC`: ordena por mayor número de fallos.

## Cómo probar (con el dataset de ejemplo)
1) Requiere Python 3.12.10 (usa solo `sqlite3` de la biblioteca estándar).
2) Desde la raíz del repo:
   ```bash
   python -m unittest -v tests/test_solution_applicant_query.py
   ```
   Este test crea una base SQLite en memoria con los datos de ejemplo del enunciado, ejecuta `applicant_query.sql` y valida que el resultado sea `("Whitney Ferrero", 6)`.
