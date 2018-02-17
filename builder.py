import markov
import wrangle
from user import User

corpus = markov.read_json()

users = {}

def build():
    user_counts = wrangle.root_transform_user_counts(corpus['user_counts'])
    user_id = wrangle.choose_user(user_counts)
    if user_id not in users:
        users[user_id] = User(user_id)
    print users[user_id].name
    print wrangle.build_text(corpus, user_id)

build()
