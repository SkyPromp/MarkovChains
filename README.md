# Markov Chains
## TODO
- Encode markov chain settings into type, so it can be pickled together with the rest.
- Pick random option with the correct length when prompting (buffer is set in generateOutput).
- Add shorter N-grams as fallback
- Option to remove rare branches
- Have everything as a primary key and then remove collision checks (still insert with batches for storage size reduction), this increases filesize, but reduces write time
- use nosql
- merge databases
- with regressing length the starts get overweighted since it first increases the length
