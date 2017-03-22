import unittest

import sys

sys.path.append('../../src')

from fbp.port import port, inport, outport


class TestFBPPort(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_port(self):
        print "test port"
        aport = port("aport")
        self.assertEqual(aport.name, "aport")
        self.assertEqual(aport.type, "String")

        aport.value = "new value"
        self.assertEqual(aport.value, "new value")

        print aport

    def test_in_port(self):
        print "test in port"
        aport = inport("aport")
        self.assertEqual(aport.name, "aport")
        self.assertEqual(aport.type, "String")
        self.assertEqual(aport.value, None)
        self.assertEqual(aport.is_required, False)
        self.assertEqual(aport.order, 0)

        aport.value = "new value"
        self.assertEqual(aport.value, "new value")

        print aport

    def test_port_link(self):
        print "test port link"
        aport = inport("in_port")
        bport = outport("out_port")

        bport.point_to(aport)
        bport.value = "new value"

        self.assertEqual(aport.value, "new value")
        self.assertEqual(bport.value, "new value")

        print aport
        print bport


if __name__ == '__main__':
    unittest.main()
