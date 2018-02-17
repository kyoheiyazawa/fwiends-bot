import markov
import random
from numpy.random import choice

corpus = markov.read_json()

# Even out differences by taking the square root of occurrence count
def root_transform_user_counts(user_counts):
    transformed_counts = {}
    for user in user_counts:
        transformed_counts[user] = int(user_counts[user] ** 0.5)
    return transformed_counts

def choose_user(user_counts):
    value_sum = sum(user_counts.values())
    probs = []
    for user in user_counts:
        probs.append(user_counts[user] / float(value_sum))
    return choice(user_counts.keys(), p=probs)

def format_quotes(message):
    quote_count = message.count('"')
    if quote_count == 1:
        index = message.index('"')
        if index == 0:
            new_msg = message + '"'
        elif index == (len(message) - 1):
            new_msg = '"' + message
        else:
            left = message[index - 1]
            right = message[index + 1]
            if left == ' ':
                new_msg = message + '"'
            elif right == ' ':
                new_msg = '"' + message
            else:
                return message
        return new_msg
    return message.replace('`', '')
        
def build_text(markov, user):
    initial_types = ['unigrams', 'unigrams', 'bigrams', 'bigrams', 'bigrams']
    type = random.choice(initial_types)
    message_words = []
    seed = random.choice(markov['chains'][user][type]['initial_{0}'.format(type)])
    message_words.append(seed)
    while True:
        next = random.choice(markov['chains'][user][type]['chains'][seed])
        if next is None:
                break
        type = random.choice(initial_types)
        if type == 'unigrams':
            seed = next
        else:
            words = seed.split()
            seed = '{0} {1}'.format(words[-1], next)
        message_words.append(next)
    message = ' '.join(message_words)
    return format_quotes(message)

def trial():
    user = choose_user(root_transform_user_counts(corpus['user_counts']))
    print build_text(corpus, user)

trial()
#print choose_writer(root_transform_user_counts(corpus['user_counts']))


