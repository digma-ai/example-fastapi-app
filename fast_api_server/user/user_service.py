from user.user_store import UserStore

class UserService:
    def __init__(self):
        self.user_store = UserStore()

    def all(self, id):
        if (id == '1'):
            raise Exception("blah")
        users = self.user_store.get_users()
        self.printusers(users)

    def print_users(self, users):
        for user in users:
            print(user.name)

    def some(self, users):
        self.print_users(users)
