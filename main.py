from pprint import pprint
from random import randint
from collections import OrderedDict


filename = "vlaamse_achternamen.txt"
start_symbol = "^"
stop_symbol = "$"
chains = OrderedDict()  # dict[tuple[

with open(filename, "r") as f:
    for line in f:
        line = line.strip()

        current_symbol = start_symbol

        for symbol in line:
            if current_symbol in chains:
                if symbol in chains[current_symbol]:
                    chains[current_symbol][symbol] += 1
                else:
                    chains[current_symbol][symbol] = 1
            else:
                chains[current_symbol] = OrderedDict([(symbol, 1)])
            
            current_symbol = symbol

        if current_symbol in chains:
            if stop_symbol in chains[current_symbol]:
                chains[current_symbol][stop_symbol] += 1
            else:
                chains[current_symbol][stop_symbol] = 1
        else:
            chains[current_symbol] = OrderedDict([(stop_symbol, 1)])

current_symbol = start_symbol
output = ""

while current_symbol != stop_symbol:
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


print(output)

