
def validate_user(username: str):
    if not username:
        raise InvalidInput('Empty username value')

    validate_authorization(username)


def validate_authorization(username: str):
    if username != 'admin':
        raise AuthorizationError()


class InvalidInput(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AuthorizationError(Exception):
    pass
