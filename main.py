from markov import MarkovChain
import sqlite3 as sql


# filename = "vlaamse_achternamen.txt"
# filename = "waalse_achternamen.txt"
# filename = "brusselse_achternamen.txt"
# filename = "belgische_achternamen.txt"
# filename = "alice_in_wonderland.txt"
# filename = "sentences_100k.txt"
# filename = "sentences.txt"
# filename = "sentences_500k.txt"
# filename = "sentences_250k.txt"
# filename = "1000-most-common-names-USA-male.txt"
# filename = "clean_sentences.txt"
# filename = "female_names.txt"
# filename = "clean_sentences_250k.txt"
# filename = "clean_sentences_500k.txt"
filename = "clean_sentences_150k.txt"
# filename = "data.txt"


length = 20
markov = MarkovChain(start_symbol="&&&&", stop_symbol="$$$$", length=length)

save_filename = f"models/buf_{length}_{filename}.db"

conn = sql.connect(save_filename)
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

conn.commit()

if not conn.execute("SELECT EXISTS (SELECT 1 FROM transitions LIMIT 1)").fetchone()[0]:
    print("Generates")
    markov.generateChains(f"data/{filename}", conn)

# buffer = "Wit"
buffer = ""

print(f"Outputs with buffer <<{buffer}>>:\n")

for i in range(3):
    output = markov.generateOutput(conn, buffer=buffer)

    # print(f"Output {i}:")
    print(output)
    print()


