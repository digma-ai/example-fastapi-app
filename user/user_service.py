from user.user_store import UserStore


class UserService:
    def __init__(self):
        self.user_store = UserStore()

    def all(self):
        users= self.user_store.get_users()
        if users:
            for user in users:
                print(user.name)
