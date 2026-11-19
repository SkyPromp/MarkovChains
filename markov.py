from random import randint
# from collections import dict
from typing import Optional, TypeAlias, Dict
from pickle import load, dump
from os.path import exists


MarkovChainType: TypeAlias = Dict[str, Dict[str, int]]


class MarkovChain:
    def __init__(self, start_symbol="^", stop_symbol="$", length=10):
        self.start_symbol = start_symbol
        self.stop_symbol = stop_symbol
        self.length = length

    def generateChains(self, filename: str) -> MarkovChainType:  # Train
        chains = dict()

        with open(filename, "r", encoding="utf-8") as f:
            print("reading")
            total_lines = sum(1 for _ in f)
            f.seek(0)

            for line_nr, line in enumerate(f):
                if line_nr % 1000 == 0:
                    print(f"Progress: {line_nr * 100 / total_lines:.2f}%")

                line = line.strip()

                current_symbol = self.start_symbol
                buffer = ""

                for i, symbol in enumerate(line):
                    buffer += symbol
                    buffer = buffer[-self.length:]

                    if current_symbol in chains:
                        if symbol in chains[current_symbol]:
                            chains[current_symbol][symbol] += 1
                        else:
                            chains[current_symbol][symbol] = 1
                    else:
                        chains[current_symbol] = dict([(symbol, 1)])
                    current_symbol = buffer

                if len(buffer) == self.length:
                    current_symbol = buffer[-self.length:]

                if current_symbol in chains:
                    if self.stop_symbol in chains[current_symbol]:
                        chains[current_symbol][self.stop_symbol] += 1
                    else:
                        chains[current_symbol][self.stop_symbol] = 1
                else:
                    chains[current_symbol] = dict([(self.stop_symbol, 1)])

        return chains

    def generateOutput(self, chains: MarkovChainType, buffer="") -> str:  # Run
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

            options = chains[current_symbol]
            choices = options.keys()
            counts = options.values()
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

    @staticmethod
    def save(object: MarkovChainType, path: str) -> None:
        with open(path, "wb") as f:
            dump(object, f)

    @staticmethod
    def load(path: str) -> Optional[MarkovChainType]:
        if exists(path):
            with open(path, "rb") as f:
                return load(f)

        return None
