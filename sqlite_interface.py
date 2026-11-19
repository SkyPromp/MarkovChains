import sqlite3 as sql


def createTable(conn: sql.Connection):
    conn.execute(
        """
            CREATE TABLE IF NOT EXISTS transitions (
                state TEXT NOT NULL,
                symbol TEXT NOT NULL,
                count INTEGER NOT NULL,
                PRIMARY KEY (state, symbol)
            ) WITHOUT ROWID
        """
    )


def insertMany(conn: sql.Connection, batch: dict[tuple[str, str], int]) -> None:
    conn.executemany("""
        INSERT INTO transitions
        VALUES (?, ?, ?)
        ON CONFLICT(state, symbol)
        DO UPDATE SET count = count + excluded.count
    """, ((state, symbol, count) for (state, symbol), count in batch.items()))


def tableHasData(conn) -> bool:
    return conn.execute("SELECT EXISTS (SELECT 1 FROM transitions LIMIT 1)").fetchone()[0]


def findMatchingSymbols(conn: sql.Connection, state: str) -> tuple[list[str], list[int]]:
    cursor = conn.execute("""
        SELECT symbol, count
        FROM transitions
        WHERE state = (?)
    """, (state,))
    rows = cursor.fetchall()

    choices = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    return choices, counts
