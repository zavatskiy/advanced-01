import unittest

from tests.test_server import TestServer
from tests.test_pkt import TestPkt

suite_server = unittest.TestLoader().loadTestsFromTestCase(TestServer)
suite_cmds = unittest.TestLoader().loadTestsFromTestCase(TestPkt)

if __name__ == '__main__':
    #unittest.TextTestRunner().run(suite_server)
    unittest.TextTestRunner().run(suite_cmds)
