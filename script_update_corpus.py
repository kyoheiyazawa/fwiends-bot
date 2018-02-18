import config
import markov

if __name__ == "__main__":
    print markov.update_json(config.channel)
else:
    print "don't import this"