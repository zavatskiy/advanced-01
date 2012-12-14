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
    """ Pack package to bytes and unpack bytes to package """
    def __init__(self, **kwargs):
        for k in list(self._fields_.keys()):
            if k == 'cmd':
                setattr(self, 'cmd', self._fields_['cmd'].cmd)
            else:
                setattr(self, k, kwargs.get(k))

    def pack(self):
        p = b''
        for k, v in self._fields_.items():
            p += str(getattr(self, k)).encode('utf-8')
        l = len(p).to_bytes(4, byteorder='big')
        return l + p

    @classmethod
    def unpack(cls, data):
        data = data.decode('utf-8')
        obj = cls()
        obj.cmd = data[0]
        if data[1:]:
            obj.data = data[1:]
        return obj


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
    def __init__(self, maxsize):
        self.maxsize = maxsize


class Feeder:
    """ Collect incoming bytes """
    def __init__(self, conn):
        self.conn = conn

    def feed(self, buf):
        buf += self.conn.recv(1024)
        if not self.pkt_len and len(buf) > 3:
            buf = self._cut_pkt_len(buf)
        if self.pkt_len and len(buf) >= self.pkt_len:
            return Feeder2.get_pkt(buf)
        else:
            return None, buf

    def _cut_pkt_len(self, buf):
        self.pkt_len = int.from_bytes(buf[:4], byteorder='big')
        return buf[4:]


class Feeder2:
    """ Construct Packet from bytes """
    @staticmethod
    def get_pkt(self, buf):
        p = Packet.unpack(buf)
        return p.cmd, buf


class Connect(Packet):
    """ Connect command """
    cmd = Cmd(CONNECT)


class Ping(Packet):
    """ Ping command """
    cmd = Cmd(PING)


class PingD(Packet):
    """ PingD command """
    cmd = Cmd(PINGD)
    data = Str(maxsize=256)


class AckQuit(Packet):
    """ AckQuit command """
    cmd = Cmd(ACKQUIT)
    data = Str(maxsize=256)


class AckFinish(Packet):
    """ AckFinish command """
    cmd = Cmd(ACKFINISH)
    data = Str(maxsize=256)
