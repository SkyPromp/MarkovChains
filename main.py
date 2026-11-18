from random import randint
from collections import OrderedDict
from typing import TypeAlias


MarkovChain: TypeAlias = OrderedDict[str, OrderedDict[str, int]]
start_symbol = "^"
stop_symbol = "$"
length = 3


def generateChains(filename: str) -> MarkovChain:
    chains = OrderedDict()

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            current_symbol = start_symbol
            buffer = ""

            for i, symbol in enumerate(line):
                buffer += symbol
                buffer = buffer[-length:]

                if current_symbol in chains:
                    if symbol in chains[current_symbol]:
                        chains[current_symbol][symbol] += 1
                    else:
                        chains[current_symbol][symbol] = 1
                else:
                    chains[current_symbol] = OrderedDict([(symbol, 1)])
                current_symbol = buffer

            if len(buffer) == length:
                current_symbol = buffer[-length:]

            if current_symbol in chains:
                if stop_symbol in chains[current_symbol]:
                    chains[current_symbol][stop_symbol] += 1
                else:
                    chains[current_symbol][stop_symbol] = 1
            else:
                chains[current_symbol] = OrderedDict([(stop_symbol, 1)])

    return chains


def generateName(chains: MarkovChain):
    current_symbol = start_symbol
    output = ""

    while current_symbol != stop_symbol:
        if current_symbol != start_symbol:
            current_symbol = output[-length:]
        options = chains[current_symbol]
        choices = options.keys()
        counts = options.values()
        total = sum(counts)
        choice = randint(1, total)

        for ch, co in zip(choices, counts):
            choice -= co

            if choice <= 0:
                if ch != stop_symbol:
                    output += ch

                current_symbol = ch

                break

    return output


filename = "vlaamse_achternamen.txt"
# filename = "waalse_achternamen.txt"
# filename = "brusselse_achternamen.txt"
# filename = "belgische_achternamen.txt"
chains = generateChains(filename)
output = generateName(chains)
print(output)
