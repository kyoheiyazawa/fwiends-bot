import config
import json
import requests
import urllib

api_base = 'https://slack.com/api/'
auth = {'Authorization': 'Bearer {0}'.format(config.token)}

def slack_request(endpoint, params={}):
    url = '{0}{1}'.format(api_base, endpoint)
    if params:
        query_str = urllib.urlencode(params)
        url += '?{0}'.format(query_str)
    response = requests.get(url, headers=auth)
    return json.loads(response.text)

def get_msgs(channel, count, iter=1):
    messages = []
    latest = None
    options = {
        'channel': channel,
        'count': count
    }
    for i in range(iter):
        print 'Request {0} in progress...'.format(i+1)
        response = slack_request('groups.history', options)['messages']
        if response:
            messages += response
            latest = response[-1]['ts']
        else:
            print messages
            return messages
        options['latest'] = latest
    return messages

def get_recent_msgs(channel, oldest):
    options = {
        'channel': channel,
        'count': 1000,
        'oldest': oldest
    }
    return slack_request('groups.history', options)['messages']

def revoke_token():
    params = {
        'token': config.token
    }
    return slack_request('auth.revoke', params)
