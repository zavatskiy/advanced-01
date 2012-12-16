import unittest

from tests.test_client01 import TestClient01
from tests.test_pkt import TestPkt

suite01 = unittest.TestSuite()
suite01.addTest(TestClient01('test_connect'))
suite01.addTest(TestClient01('test_ping'))
suite01.addTest(TestClient01('test_pingd'))
suite01.addTest(TestClient01('test_quit'))
suite01.addTest(TestClient01('test_finish'))

suite_cmds = unittest.TestSuite()
suite_cmds.addTest(TestPkt('test_not_cmd'))
suite_cmds.addTest(TestPkt('test_connect_cmd'))
suite_cmds.addTest(TestPkt('test_connect_pack'))
suite_cmds.addTest(TestPkt('test_connect_unpack'))
suite_cmds.addTest(TestPkt('test_ping_cmd'))
suite_cmds.addTest(TestPkt('test_ping_pack'))
suite_cmds.addTest(TestPkt('test_ping_unpack'))
suite_cmds.addTest(TestPkt('test_pingd_cmd'))
suite_cmds.addTest(TestPkt('test_pingd_pack'))
suite_cmds.addTest(TestPkt('test_pingd_unpack'))
suite_cmds.addTest(TestPkt('test_quit_cmd'))
suite_cmds.addTest(TestPkt('test_quit_pack'))
suite_cmds.addTest(TestPkt('test_quit_unpack'))
suite_cmds.addTest(TestPkt('test_finish_cmd'))
suite_cmds.addTest(TestPkt('test_finish_pack'))
suite_cmds.addTest(TestPkt('test_finish_unpack'))

if __name__ == '__main__':
    #unittest.TextTestRunner().run(suite01)
    unittest.TextTestRunner().run(suite_cmds)
