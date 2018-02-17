import api
import config

msgs = api.get_msgs(config.channel, 1, 1)
print msgs[-1]
# for msg in msgs:
#     print msg

blank_markov = {
    'users': [],
    'user_counts': [],
    'chains': {},
}

def init_markov_json(channel, count, iterations):
    messages = api.get_msgs(channel, count, iterations)
    with open('markov.json', 'wb') as outfile:
        json.dump(get_markov_obj(blank_markov, messages), outfile)

def update_markov_json():
    print 'durrr'

def get_markov_obj(markov, msgs):
    markov['latest_ts'] = msgs[-1]['ts']
    for msg in msgs:
        if 'subtype' in msg:
            continue
        if 'http' in msg['text']:
            continue
        if 'iOS>' in msg['text']:
            continue
        user = msg['user']
        markov['user_counts'].append(user)

        if user not in markov['users']:
            markov['users'].append(user)
            markov['chains'][user] = {
                'unigrams': {
                    'initial_unigrams': [],
                    'chains': {}
                },
                'bigrams': {
                    'initial_bigrams': [],
                    'chains': {}
                }
            }

        words = msg['text'].split()
        list_len = len(words)
        if words:
            markov['chains'][user]['unigrams']['initial_unigrams'].append(words[0])
        if list_len > 1:
            markov['chains'][user]['bigrams']['initial_bigrams'].append(u'{0} {1}'.format(words[0], words[1]))

        # unigrams
        for index, word in enumerate(words):
            next_word = None
            if index < (list_len - 1):
                next_word = words[index + 1]
            if word not in markov['chains'][user]['unigrams']['chains']:
                markov['chains'][user]['unigrams']['chains'][word] = [next_word]
            else:
                markov['chains'][user]['unigrams']['chains'][word].append(next_word)

        #bigrams
        for index, word in enumerate(words):
            if index > (list_len - 2):
                break
            bigram = u'{0} {1}'.format(word, words[index + 1])
            next_word = None
            if index < (list_len - 2):
                next_word = words[index + 2]
            if bigram not in markov['chains'][user]['bigrams']['chains']:
                markov['chains'][user]['bigrams']['chains'][bigram] = [next_word]
            else:
                markov['chains'][user]['bigrams']['chains'][bigram].append(next_word)
    return markov

