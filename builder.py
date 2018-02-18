import io
import markov
import wrangle
from jinja2 import Environment, FileSystemLoader, select_autoescape
from user import User

def build(count):
    env = Environment(
        loader=FileSystemLoader('templates/'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('chat.html')
    corpus = markov.read_json()
    users = {}
    user_counts = wrangle.root_transform_user_counts(corpus['user_counts'])    
    msgs = []
    render_data = {
        'user_block': []
    }
    for i in range(0, count):
        user_id = wrangle.choose_user(user_counts)
        if user_id not in users:
            users[user_id] = User(user_id)
        text = wrangle.build_text(corpus, user_id)
        msgs.append({
            'user_id': user_id,
            'text': text
        })
    prev_user = None
    append_block = {}
    for msg in msgs:
        user = users[msg['user_id']]
        if msg['user_id'] != prev_user:
            if append_block:
                render_data['user_block'].append(append_block)
            append_block['name'] = user.name
            append_block['avatar'] = user.avatar_72
            append_block['msgs'] = []
        append_block['msgs'].append(msg['text'])
        prev_user = msg['user_id']
    render_data['user_block'].append(append_block)
    html = template.render(data=render_data)
    with io.open('jinja2_chat.html', mode='w', encoding='utf-8') as outfile:
        outfile.write(unicode(html))
