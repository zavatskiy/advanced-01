import unittest

from tests.test_client01 import TestClient01
from tests.test_pkt import TestPkt

suite01 = unittest.TestSuite()
suite01.addTest(TestClient01('test_connect'))
suite01.addTest(TestClient01('test_ping'))
suite01.addTest(TestClient01('test_pingd'))
suite01.addTest(TestClient01('test_quit'))
suite01.addTest(TestClient01('test_finish'))

suite02 = unittest.TestSuite()
suite02.addTest(TestPkt('test_connect_cmd'))
#suite02.addTest(TestPkt('test_connect_pack'))
#suite02.addTest(TestPkt('test_connect_unpack'))
#suite02.addTest(TestPkt('test_ping'))
#suite02.addTest(TestPkt('test_pingd'))
#suite02.addTest(TestPkt('test_quit'))
#suite02.addTest(TestPkt('test_finish'))

if __name__ == '__main__':
    #unittest.TextTestRunner().run(suite01)
    unittest.TextTestRunner().run(suite02)
