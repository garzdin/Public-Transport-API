from json import JSONEncoder

__all__ = ['ClassEncoder']

class ClassEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
