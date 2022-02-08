class UserStore:
    def get_users(self):
        return None


class InMemoryUserStore1(UserStore):
    def get_users(self):
        raise ValueError('invalid value')


class InMemoryUserStore2(UserStore):
    def get_users(self):
        raise ValueError('invalid value')
