from random import randint
from typing import Optional, TypeAlias, Dict
from pickle import load, dump
from os.path import exists
from sys import version_info
import sqlite3 as sql


class MarkovChain:
    def __init__(self, start_symbol="^", stop_symbol="$", length=10):
        self.start_symbol = start_symbol
        self.stop_symbol = stop_symbol
        self.length = length

    def generateChains(self, filename: str, conn: sql.Connection):
        # batched_inserts = []
        transitions = {}
        batch_size = 50000

        with open(filename, "r", encoding="utf-8") as f:
            # ------- Progress tracker, optional
            total_lines = sum(1 for _ in f)
            f.seek(0)
            # ------- Progress tracker, optional

            for line_nr, line in enumerate(f):
                # ------- Progress tracker, optional
                if line_nr % 1000 == 0:
                    print(f"Progress: {line_nr * 100 / total_lines:.2f}%")
                # ------- Progress tracker, optional

                line = line.strip()

                current_symbol = self.start_symbol
                buffer = ""

                for i, symbol in enumerate(line):
                    buffer += symbol
                    buffer = buffer[-self.length:]

                    # batched_inserts.append((current_symbol, symbol, 1))
                    transitions[(current_symbol, symbol)] = transitions.get((current_symbol, symbol), 0) + 1
                    current_symbol = buffer

                transitions[(current_symbol, self.stop_symbol)] = transitions.get((current_symbol, self.stop_symbol), 0) + 1
                # batched_inserts.append((current_symbol, self.stop_symbol, 1))
                
                if line_nr % batch_size == 0:
                    conn.executemany("""
                        INSERT INTO transitions
                        VALUES (?, ?, ?)
                        ON CONFLICT(state, symbol)
                        DO UPDATE SET count = count + excluded.count
                    """, ((state, symbol, count) for (state, symbol), count in transitions.items()))
                    transitions.clear()

        conn.executemany("""
            INSERT INTO transitions
            VALUES (?, ?, ?)
            ON CONFLICT(state, symbol)
            DO UPDATE SET count = count + excluded.count
        """, ((state, symbol, count) for (state, symbol), count in transitions.items()))
        conn.commit()

    def generateOutput(self, conn: sql.Connection, buffer="") -> str:  # Run
        if buffer == "":
            current_symbol = self.start_symbol

            if len(current_symbol) != self.length:
                pass  # TODO: pick random option with the correct length
        else:
            current_symbol = buffer

        output = buffer

        while current_symbol != self.stop_symbol:
            if current_symbol != self.start_symbol:
                current_symbol = output[-self.length:]

            cursor = conn.execute("""
                SELECT symbol, count
                FROM transitions
                WHERE state = (?)
            """, (current_symbol,))
            rows = cursor.fetchall()

            choices = [row[0] for row in rows]
            counts = [row[1] for row in rows]
            total = sum(counts)
            choice = randint(1, total)

            for ch, co in zip(choices, counts):
                choice -= co

                if choice <= 0:
                    if ch != self.stop_symbol:
                        output += ch

                    current_symbol = ch

                    break

        return output

