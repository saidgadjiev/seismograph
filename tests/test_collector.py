import unittest
from seismograph.collector import *


class TestCollector(unittest.TestCase):
    def test_get_shuffle(self):
        get_shuffle(2)


if __name__ == "__main__":
    unittest.main()
