from markov import MarkovChain
import tracemalloc


filename = "vlaamse_achternamen.txt"
# filename = "waalse_achternamen.txt"
# filename = "brusselse_achternamen.txt"
# filename = "belgische_achternamen.txt"
# filename = "alice_in_wonderland.txt"
# filename = "sentences_100k.txt"
filename = "sentences.txt"
# filename = "sentences_500k.txt"
# filename = "sentences_250k.txt"
# filename = "1000-most-common-names-USA-male.txt"


length = 8
markov = MarkovChain(start_symbol="&&&&", stop_symbol="$$$$", length=length)

save_filename = f"models/buf_{length}_{filename}.pkl"

if chains := MarkovChain.load(save_filename):
    print(f"Loads: {save_filename}")
else:
    print("Generates")
    chains = markov.generateChains(filename)
    MarkovChain.save(chains, path=save_filename)


# buffer = "Wit"
buffer = ""

print(f"Outputs with buffer <<{buffer}>>:\n")

for i in range(3):
    print(f"Output {i}:")
    output = markov.generateOutput(chains, buffer=buffer)

    print()
    print(output)


