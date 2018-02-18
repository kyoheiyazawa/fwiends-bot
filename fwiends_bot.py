import builder
import config
import markov

def initialize_json():
    markov.init_json(config.channel, 2, 10)

if __name__ == "__main__":
    #initialize_json()
    builder.build(4)
