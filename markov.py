import api
import io
import json

blank_markov = {
    'user_counts': {},
    'chains': {},
}

def init_json(channel, count, iterations):
    messages = api.get_msgs(channel, count, iterations)
    with io.open('markov.json', mode='w', encoding='utf-8') as outfile:
        data = json.dumps(get_markov_obj(blank_markov, messages), ensure_ascii=False, encoding='utf-8')
        outfile.write(unicode(data))

def update_json(channel):
    with io.open('markov.json', mode='r', encoding='utf-8') as markov_json:
        markov = json.load(markov_json)
    messages = api.get_recent_msgs(channel, markov['latest_ts'])
    if messages:        
        new_markov = get_markov_obj(markov, messages)
        with io.open('markov.json', 'w', encoding='utf-8') as outfile:
            data = json.dumps(new_markov, ensure_ascii=False, encoding='utf-8')
            outfile.write(unicode(data))
        return 'Update complete - {0} messages added to markov.json.'.format(len(messages))
    else:
        return 'No new messages - markov.json unchanged.'

def read_json():
    with io.open('markov.json', mode='r', encoding='utf-8') as markov_json:
        markov = json.load(markov_json)
    return markov

def get_markov_obj(markov, msgs):
    markov['latest_ts'] = msgs[0]['ts']
    for msg in msgs:
        if u'subtype' in msg:
            continue
        if u'http' in msg['text']:
            continue
        if u'iOS>' in msg['text']:
            continue
        user = msg['user']

        if user not in markov['user_counts']:
            markov['user_counts'][user] = 0
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
        markov['user_counts'][user] += 1

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
