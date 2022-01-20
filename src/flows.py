class C:
    def execute(self):
        try:
            B().execute()
        except Exception:
            raise ValueError('C')


class B:
    def execute(self):
        E().execute()


class A:
    def execute(self):
        try:
            C().execute()
        except Exception:
            raise ValueError('A')


class E:
    def execute(self):
        raise NotImplementedError("E")


class D:
    def execute(self):
        try:
            C().execute()
        except Exception:
            raise ValueError('D')


def recursive_call(deep: int = 5):
    parameter = None if deep == 1 or deep == 0 else 'some value'
    if deep == 0:
        raise Exception("stopped")
    try:
        recursive_call(deep-1)
    except Exception as ex:
        if deep == 3:
            raise ValueError('continue')
        raise ex