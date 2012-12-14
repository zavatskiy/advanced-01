import unittest

import pkt


class TestPkt(unittest.TestCase):

    def test_empty(self):
        pass

    def test_non_cmd(self):
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
        self.assertEqual(pkt.Connect, type(p))
        self.assertEqual(pkt.CONNECT, p.cmd)

    def test_ping(self):
        pass

    def test_pingd(self):
        pass

    def test_quit(self):
        pass

    def test_quitd(self):
        pass

    def test_finish(self):
        pass
