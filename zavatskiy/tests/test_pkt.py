import unittest

import pkt


class TestPkt(unittest.TestCase):

    def test_not_cmd(self):
        pass

    def test_reg_cmds(self):
        pass

    def test_connect_cmd(self):
        p = pkt.Connect()
        self.assertEqual(pkt.CONNECT, p.cmd)

    def test_connect_pack(self):
        connect = pkt.Connect()
        self.assertEqual(b'\x00\x00\x00\x011', connect.pack())

    def test_connect_unpack(self):
        p = pkt.Packet.unpack(b'1')
        self.assertEqual(pkt.CONNECT, p.cmd)
        self.assertEqual(pkt.Connect, type(p))

    def test_ping_cmd(self):
        p = pkt.Ping()
        self.assertEqual(pkt.PING, p.cmd)

    def test_ping_pack(self):
        ping = pkt.Ping()
        self.assertEqual(b'\x00\x00\x00\x012', ping.pack())

    def test_ping_unpack(self):
        p = pkt.Packet.unpack(b'2')
        self.assertEqual(pkt.PING, p.cmd)
        self.assertEqual(pkt.Ping, type(p))

    def test_pingd_cmd(self):
        p = pkt.PingD(data='DATA')
        self.assertEqual(pkt.PINGD, p.cmd)
        self.assertEqual('DATA', p.data)

    def test_pingd_pack(self):
        pingd = pkt.PingD(data='DATA')
        self.assertEqual(b'\x00\x00\x00\x053DATA', pingd.pack())

    def test_pingd_unpack(self):
        p = pkt.Packet.unpack(b'3DATA')
        self.assertEqual(pkt.PINGD, p.cmd)
        self.assertEqual('DATA', p.data)
        self.assertEqual(pkt.PingD, type(p))

    def test_quit_cmd(self):
        p = pkt.Quit()
        self.assertEqual(pkt.QUIT, p.cmd)

    def test_quit_pack(self):
        quit = pkt.Quit()
        self.assertEqual(b'\x00\x00\x00\x014', quit.pack())

    def test_quit_unpack(self):
        p = pkt.Packet.unpack(b'4')
        self.assertEqual(pkt.QUIT, p.cmd)
        self.assertEqual(pkt.Quit, type(p))

    def test_quitd_cmd(self):
        p = pkt.QuitD(data='QUIT')
        self.assertEqual(pkt.QUITD, p.cmd)
        self.assertEqual('QUIT', p.data)

    def test_quitd_pack(self):
        quitd = pkt.QuitD(data='QUIT')
        self.assertEqual(b'\x00\x00\x00\x015', quit.pack())

    def test_quitd_unpack(self):
        p = pkt.Packet.unpack(b'5QUIT')
        self.assertEqual(pkt.QUITD, p.cmd)
        self.assertEqual(b'QUIT', p.data)
        self.assertEqual(pkt.QuitD, type(p))

    def test_finish_cmd(self):
        p = pkt.Finish()
        self.assertEqual(pkt.FINISH, p.cmd)

    def test_finish_pack(self):
        finish = pkt.Finish()
        self.assertEqual(b'\x00\x00\x00\x016', finish.pack())

    def test_finish_unpack(self):
        p = pkt.Packet.unpack(b'6')
        self.assertEqual(pkt.FINISH, p.cmd)
        self.assertEqual(pkt.Finish, type(p))
