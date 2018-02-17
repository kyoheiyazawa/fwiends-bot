import random
from numpy.random import choice

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

def get_user_freq_category(user, user_counts):
    user_freq = user_counts[user]
    min_value = user_counts[min(user_counts, key=user_counts.get)]
    max_value = user_counts[max(user_counts, key=user_counts.get)]
    spread = max_value - min_value
    if user_freq > max_value - (spread * 0.33):
        return 'high'
    elif user_freq > max_value - (spread * 0.66):
        return 'med'
    else:
        return 'low'

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
        
def build_text(markov_dict, user):
    # Vary prevalence of bigrams based on user post frequency
    initial_types_mapping = {
        'high': ['unigrams', 'unigrams', 'bigrams', 'bigrams', 'bigrams'],
        'med': ['unigrams','bigrams'],
        'low': ['unigrams', 'unigrams', 'bigrams']                
    }
    user_freq = get_user_freq_category(user, markov_dict['user_counts'])
    initial_types = initial_types_mapping[user_freq]
    type = random.choice(initial_types)
    message_words = []
    seed = random.choice(markov_dict['chains'][user][type]['initial_{0}'.format(type)])
    message_words.append(seed)
    while True:
        next = random.choice(markov_dict['chains'][user][type]['chains'][seed])
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
