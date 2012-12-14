import time
import socket

import pkt
from work.helpers import make_message, parse_message


class Client01:

    def __init__(self, host='127.0.0.1', port=6666):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, data):
        self.socket.sendall(data)

    def recive(self):
        buf = b''
        feeder = pkt.Feeder(self.socket)
        cmd = None
        while not cmd:
            cmd, buf = feeder.feed(buf)
        return cmd, buf

    def close(self):
        self.socket.close()


if __name__ == '__main__':

    client = Client01()
    client.send(pkt.Connect().pack())
    ans = client.recive()

    print('> '.join([ans[0], ans[1]]))

    while True:
        data = raw_input('pingd> ')
        client.send(pkt.PingD(data).pack())

        ans = client.recive()
        if not ans[0]:
            client.close()
        if ans[0] in ['ackquit', 'ackfinish']:
            break

        print('> '.join([ans[0], ans[1]]))

    client.close()
