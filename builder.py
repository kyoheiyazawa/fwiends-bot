import markov
import wrangle
from user import User

corpus = markov.read_json()

def build():
    user_counts = wrangle.root_transform_user_counts(corpus['user_counts'])
    user_id = wrangle.choose_user(user_counts)
    user = User(user_id)
    print user.name
    print wrangle.build_text(corpus, user_id)

build()
