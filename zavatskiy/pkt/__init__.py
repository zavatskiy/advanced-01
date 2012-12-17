from collections import OrderedDict

from .fields import Field, Cmd, Str

CONNECT = 1
PING = 2
PINGD = 3
QUIT = 4
QUITD = 5
FINISH = 6

CONNECTED = 7
PONG = 8
PONGD = 9
ACKQUIT = 10
ACKQUITD = 11
ACKFINISH = 12


class MetaPacket(type):
    """Register commands.

    Checks for compliance with the order of the fields and
    the lack of a required field.
    """

    cmds = dict()
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __init__(cls, name, bases, dct):
        if cls.__name__ != 'Packet':
            type.__init__(cls, name, bases, dct)
            cls.fields = OrderedDict()
            cmd = False
            for k, v in dct.items():
                if isinstance(v, Cmd):
                    assert v.cmd not in list(cls.cmds.keys()), 'Command repeat.'
                    cls.cmds[v.cmd] = cls
                    cmd = True
                if isinstance(v, Field):
                    v.name = k
                    cls.fields[k] = v

            if not cmd:
                assert cmd, 'Command not exists.'

            assert isinstance(list(cls.fields.values())[0], Cmd), (
                'Command must be the first argument.')


class Packet(metaclass=MetaPacket):
    """Abstract handler.

    Pack fields to bytes. Unpack bytes to packet."""

    def __init__(self, **kwargs):
        setattr(self, 'cmd', list(self.fields.values())[0].cmd)
        for k in list(self.fields)[1:]:
            setattr(self, k, kwargs.get(k))

    def pack(self):
        """Pack fields to bytes."""
        p = b''
        for k, v in self.fields.items():
            p += str(getattr(self, k)).encode('utf-8')
        l = len(p).to_bytes(4, byteorder='big')
        return l + p

    @classmethod
    def unpack(cls, data):
        """Unpack bytes to packet."""
        data = data.decode('utf-8')
        cmd = cls.cmds.get(int(data[0]))

        kwargs = dict()
        for k in list(cmd.fields.keys())[1:]:
            kwargs[k] = data[1:]
        return cmd(**kwargs)


class Feeder:
    """Collect incoming bytes.

    Gets a chunk of incoming buffer.
    """

    def __init__(self, socket):
        self.socket = socket
        self.pkt_len = 0

    def feed(self, buf):
        """Process incoming bytes."""
        buf += self.socket.recv(1024)
        if not self.pkt_len and len(buf) >= 4:
            buf = self._cut_pkt_len(buf)
        if self.pkt_len and len(buf) >= self.pkt_len:
            return Feeder2.get_pkt(buf)
        else:
            return None, buf

    def _cut_pkt_len(self, buf):
        """Store buffer length and return only data in buffer."""
        self.pkt_len = int.from_bytes(buf[:4], byteorder='big')
        return buf[4:]


class Feeder2:
    """ Construct Packet from bytes """

    @staticmethod
    def get_pkt(buf):
        p = Packet.unpack(buf)
        return p.cmd, buf


class Connected(Packet):
    """ Connected command."""

    cmd = Cmd(CONNECTED)


class Connect(Packet):
    """Connect command."""

    cmd = Cmd(CONNECT)
    ans = Connected


class Pong(Packet):
    """Pong command."""

    cmd = Cmd(PONG)


class Ping(Packet):
    """Ping command."""

    cmd = Cmd(PING)
    ans = Pong


class PongD(Packet):
    """PongD command."""

    cmd = Cmd(PONGD)
    data = Str(maxsize=256)


class PingD(Packet):
    """PingD command."""

    cmd = Cmd(PINGD)
    data = Str(maxsize=256)
    ans = PongD


class AckQuit(Packet):
    """AckQuit command."""

    cmd = Cmd(ACKQUIT)
    data = Str(maxsize=256)


class Quit(Packet):
    """Quit command."""

    cmd = Cmd(QUIT)
    ans = AckQuit


class AckQuitD(Packet):
    """AckQuit command."""

    cmd = Cmd(ACKQUITD)
    data = Str(maxsize=256)


class QuitD(Packet):
    """Quit command."""

    cmd = Cmd(QUITD)
    data = Str(maxsize=256)
    ans = AckQuitD


class AckFinish(Packet):
    """AckFinish command."""

    cmd = Cmd(ACKFINISH)
    data = Str(maxsize=256)


class Finish(Packet):
    """Finish command."""

    cmd = Cmd(FINISH)
    ans = AckFinish
