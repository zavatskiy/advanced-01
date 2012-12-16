from collections import OrderedDict

from .fields import Field, Cmd, Str

CONNECT = 0
PING = 1
PINGD = 2
QUIT = 3
FINISH = 4

CONNECTED = 5
PONG = 6
PONGD = 7
ACKQUIT = 8
ACKFINISH = 9


class MetaPacket(type):
    cmds = dict()
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __init__(cls, name, bases, dct):
        type.__init__(cls, name, bases, dct)
        cls.fields = OrderedDict()
        for k, v in dct.items():
            if isinstance(v, Cmd):
                cls.cmds[v.cmd] = cls
            if isinstance(v, Field):
                v.name = k
                cls.fields[k] = v


class Packet(metaclass=MetaPacket):
    """ Pack package to bytes and unpack bytes to package """
    def __init__(self, **kwargs):
        setattr(self,
                self.fields.keys()[0],
                self.fields.values()[0])
        for k, v in self.fields[1:]:
            setattr(self, k, kwargs.get(k))

    def pack(self):
        p = b''
        for k, v in self._fields_.items():
            p += str(getattr(self, k)).encode('utf-8')
        l = len(p).to_bytes(4, byteorder='big')
        return l + p

    @classmethod
    def unpack(cls, data):
        #: TODO Return cmd obj
        data = data.decode('utf-8')
        obj = cls()
        print(cls)
        obj.cmd = int(data[0])
        if data[1:]:
            obj.data = data[1:]
        return obj


class Feeder:
    """ Collect incoming bytes """
    def __init__(self, socket):
        self.socket = socket
        self.pkt_len = 0

    def feed(self, buf):
        buf += self.socket.recv(1024)
        if not self.pkt_len and len(buf) >= 4:
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
    def get_pkt(buf):
        p = Packet.unpack(buf)
        return p.cmd, buf


class Connected(Packet):
    """ Connected command """
    cmd = Cmd(CONNECTED)


class Connect(Packet):
    """ Connect command """
    cmd = Cmd(CONNECT)
    ans = Connected


class Pong(Packet):
    """ Pong command """
    cmd = Cmd(PONG)


class Ping(Packet):
    """ Ping command """
    cmd = Cmd(PING)
    ans = Pong


class PongD(Packet):
    """ PongD command """
    cmd = Cmd(PONGD)
    data = Str(maxsize=256)


class PingD(Packet):
    """ PingD command """
    cmd = Cmd(PINGD)
    data = Str(maxsize=256)
    ans = PongD


class AckQuit(Packet):
    """ AckQuit command """
    cmd = Cmd(ACKQUIT)
    data = Str(maxsize=256)


class Quit(Packet):
    """ Quit command """
    cmd = Cmd(QUIT)
    data = Str(maxsize=256)
    ans = AckQuit


class AckFinish(Packet):
    """ AckFinish command """
    cmd = Cmd(ACKFINISH)
    data = Str(maxsize=256)


class Finish(Packet):
    """ Finish command """
    cmd = Cmd(FINISH)
    data = Str(maxsize=256)
    ans = AckFinish
