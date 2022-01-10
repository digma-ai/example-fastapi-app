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
