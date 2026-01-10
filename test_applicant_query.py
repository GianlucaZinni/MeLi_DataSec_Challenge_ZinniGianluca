# Tests for applicant_query.sql using Python 3.12.10 and sqlite3
import sqlite3
import unittest
from pathlib import Path


class TestApplicantQuery(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self._create_schema()
        self._load_sample_data()

    def tearDown(self):
        self.conn.close()

    def _create_schema(self):
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE customers (
                id SMALLINT,
                first_name VARCHAR(64),
                last_name VARCHAR(64)
            );
            CREATE TABLE campaigns (
                id SMALLINT,
                customer_id SMALLINT,
                name VARCHAR(64)
            );
            CREATE TABLE events (
                dt VARCHAR(19),
                campaign_id SMALLINT,
                status VARCHAR(64)
            );
            """
        )
        self.conn.commit()

    def _load_sample_data(self):
        cur = self.conn.cursor()
        cur.executemany(
            "INSERT INTO customers (id, first_name, last_name) VALUES (?, ?, ?);",
            [
                (1, "Whitney", "Ferrero"),
                (2, "Dickie", "Romera"),
            ],
        )
        cur.executemany(
            "INSERT INTO campaigns (id, customer_id, name) VALUES (?, ?, ?);",
            [
                (1, 1, "Upton Group"),
                (2, 1, "Roob, Hudson and Rippin"),
                (3, 1, "McCullough, Rempel and Larson"),
                (4, 1, "Lang and Sons"),
                (5, 2, "Ruecker, Hand and Haley"),
            ],
        )
        cur.executemany(
            "INSERT INTO events (dt, campaign_id, status) VALUES (?, ?, ?);",
            [
                ("2021-12-02 13:52:00", 1, "failure"),
                ("2021-12-02 08:17:48", 2, "failure"),
                ("2021-12-02 08:18:17", 2, "failure"),
                ("2021-12-01 11:55:32", 3, "failure"),
                ("2021-12-01 06:53:16", 4, "failure"),
                ("2021-12-02 04:51:09", 4, "failure"),
                ("2021-12-01 06:34:04", 5, "failure"),
                ("2021-12-02 03:21:18", 5, "failure"),
                ("2021-12-01 03:18:24", 5, "failure"),
                ("2021-12-02 15:32:37", 1, "success"),
                ("2021-12-01 04:23:20", 1, "success"),
                ("2021-12-02 06:53:24", 1, "success"),
                ("2021-12-02 08:01:02", 2, "success"),
                ("2021-12-01 15:57:19", 2, "success"),
                ("2021-12-02 16:14:34", 3, "success"),
                ("2021-12-02 21:56:38", 3, "success"),
                ("2021-12-01 05:54:43", 4, "success"),
                ("2021-12-02 17:56:45", 4, "success"),
                ("2021-12-02 11:56:50", 4, "success"),
                ("2021-12-02 06:08:20", 5, "success"),
            ],
        )
        self.conn.commit()

    def test_query_outputs_expected_customer(self):
        sql_path = Path("applicant_query.sql")
        query_text = sql_path.read_text()
        cur = self.conn.cursor()
        cur.execute(query_text)
        rows = cur.fetchall()
        self.assertEqual(rows, [("Whitney Ferrero", 6)])


if __name__ == "__main__":
    unittest.main()
