import config
import markov
import sys

usage = "script_build_corpus.py <number of messages to grab in multiples of 1000>"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print usage
        sys.exit()
    print "Making markov.json..."
    markov.init_json(config.channel, 1000, int(sys.argv[1]))
    print "markov.json created."    
else:
    print "don't import this"