import api

class User:
    def __init__(self, user):
        self.user = user
        self.info = api.get_user_info(user)
        self.name = self.info['real_name']
        self.avatar_72 = self.info['profile']['image_72']