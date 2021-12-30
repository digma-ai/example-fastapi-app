from user.user_store import UserStore


class UserService:
    def __init__(self):
        self.user_store = UserStore()

    def all(self):
        return self.user_store.get_users()