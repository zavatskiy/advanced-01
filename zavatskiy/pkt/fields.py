class Field:
    def __get__(self, obj, owner):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value


class Cmd(Field):
    """ Command field """
    def __init__(self, cmd):
        self.cmd = cmd


class Str(Field):
    """ String field """
    def __init__(self, maxsize):
        self.maxsize = maxsize


class Int(Field):
    """ Integer field """
