from random import randint
import sqlite3 as sql
from sqlite_interface import findMatchingSymbols, insertMany


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
                    insertMany(conn, transitions)
                    transitions.clear()

        insertMany(conn, transitions)
        conn.commit()

    def generateOutput(self, conn: sql.Connection, buffer="") -> str:  # Run
        if buffer == "":
            current_symbol = self.start_symbol

            if len(current_symbol) != self.length:
                pass  # TODO: pick random option with the correct length
        else:
            current_symbol = buffer[-self.length:]

        output = buffer

        while current_symbol != self.stop_symbol:
            if current_symbol != self.start_symbol:
                current_symbol = output[-self.length:]

            choices, counts = findMatchingSymbols(conn, current_symbol)
            total = sum(counts)
            if total == 0:
                print(f"Buffer <<{buffer}>> could not be found!")
                exit()
            choice = randint(1, total)

            for ch, co in zip(choices, counts):
                choice -= co

                if choice <= 0:
                    if ch != self.stop_symbol:
                        output += ch

                    current_symbol = ch

                    break

        return output

