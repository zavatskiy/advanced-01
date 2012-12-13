from collections import OrderedDict

CONNECT = 1
PING = 2
PINGD = 3
ACKQUIT = 4
ACKFINISH = 5

class Field:
    def set_name(self, name):
        self.name = name

    def __get__(self, obj, owner):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value


class RegCmds(OrderedDict):
    def __init__(self, bases):
        super().__init__()
        self.fields = {}
        for b in bases:
            if issubclass(b, Packet):
                self.fields.update(b._fields_)

    def __setitem__(self, key, val):
        super().__setitem__(key, val)
        if isinstance(val, Field):
            val.set_name(key)
            self.fields[key] = val


class MetaPacket(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return RegCmds(bases)

    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        cls._fields_ = dct.fields


class Packet(metaclass=MetaPacket):
    def __init__(self, **kwargs):
        pass

    def pack(self):
        pass

    @classmethod
    def unpack(cls, data):
        return cls.data


class Cmd(Field):
    def __init__(self, command):
        self.command = command


class Str(Field):
    def __init__(self, maxsize):
        self.maxsize = maxsize


class Int(Field):
    def __init__(self, maxsize):
        self.maxsize = maxsize


class Feeder:
    pass


class Connect(Packet):
    cmd = Cmd(CONNECT)


class Ping(Packet):
    cmd = Cmd(PING)


class PingD(Packet):
    cmd = Cmd(PINGD)
    data = Str(maxsize=256)


class AckQuit(Packet):
    cmd = Cmd(ACKQUIT)
    data = Str(maxsize=256)


class AckFinish(Packet):
    cmd = Cmd(ACKFINISH)
    data = Str(maxsize=256)
