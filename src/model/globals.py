import queue


class Globals:
    def __init__(self):
        self._error_q = queue.Queue()
        self._processed_q = queue.Queue()

    def get_error_q(self):
        return self._error_q

    def get_processed_q(self):
        return self._processed_q

class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class GlobalQs:
    __instance = None

    @staticmethod
    def instance():
        if GlobalQs.__instance is None:
            GlobalQs.__instance = GlobalQs()
        return GlobalQs.__instance

    def __init__(self):
        self._error_q = queue.Queue()
        self._processed_q = queue.Queue()

    def get_error_q(self):
        return self._error_q

    def get_processed_q(self):
        return self._processed_q

