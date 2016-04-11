import unittest
from contextlib import GeneratorContextManager

from mock import Mock, MagicMock
from seismograph.ext.alchemy import DBClient
from seismograph.ext.alchemy.registry import register_engine


class TestExtension(unittest.TestCase):
    def setUp(self):
        self.dbClient = DBClient()
        self.test_data = [1, 2, 3, 4, 5]
        for i in range(3):
            engine = Mock()
            engine.name = "ENGINE" + str(i)
            connect = MagicMock()
            connect.name = "test_connect" + str(i)
            connect.execute = MagicMock(return_value=self.test_data)
            transaction = FakeTransaction()
            connect.begin = MagicMock(return_value=transaction)
            engine.connect = Mock(return_value=connect)
            register_engine(i, engine)

    @unittest.skip("demonstrating skipping")
    def test_get_connection(self):
        self.assertEqual("test_connect0", self.dbClient.get_connection(0).name)

    @unittest.skip("demonstrating skipping")
    def test_read(self):
        test_generator = self.dbClient.read(0)
        self.assertIsInstance(test_generator, GeneratorContextManager)
        result = test_generator.__enter__().return_value

        for i in range(5):
            self.assertEqual(self.test_data[i], result[i])

    @unittest.skip("demonstrating skipping")
    def test_write(self):
        test_generator = self.dbClient.write(0)
        self.assertIsInstance(test_generator, GeneratorContextManager)

        with self.dbClient.write(0) as result:
            for res in result:
                pass
        transaction = self.dbClient.get_connection(0).begin()
        self.assertEqual("commit", transaction.status)


class FakeTransaction:
    def __init__(self):
        self.status = None

    @property
    def status(self):
        return self.status

    def commit(self):
        self.status = "commit"

    def rollback(self):
        self.status = "rollback"
