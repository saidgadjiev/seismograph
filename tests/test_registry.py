import unittest
from seismograph.ext.alchemy.registry import *


class TestRegistry(unittest.TestCase):
    TEST_SESSION = 'TestSession'
    TEST_ENGINE = 'TestEngine'

    def test_register_and_get_engine(self):
        register_engine(0, self.TEST_ENGINE)
        self.assertEqual(self.TEST_ENGINE, get_engine(0))

    def test_engine_not_found(self):
        with self.assertRaises(InvalidBindKey):
            get_engine(1)

    def test_register_and_get_session(self):
        register_session(self.TEST_SESSION)
        self.assertEqual(self.TEST_SESSION, get_session())

    def test_session_is_none(self):
        register_session(None)
        with self.assertRaises(RuntimeError):
            get_session()


if __name__ == "__main__":
    unittest.main()
