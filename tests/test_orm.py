import unittest
import mock


class FakeSession:
    def __init__(self):
        self.instance = None
        self.statusdelete = None
        self.statusadd = None
        self.statuscommit = None
        self.statusrefresh = None
        self.testdata = [1, 2, 3, 4]
        query = mock.Mock(name="queryTest")
        self.query = mock.Mock(return_value=query)
        query.get = mock.Mock(return_value='testing get')
        filter_by = mock.Mock(name='filterTest')
        query.filter_by = mock.Mock(return_value=filter_by)
        filter_by.first = mock.Mock(return_value='testing get_by')
        offset = mock.Mock(name='offsetTest')
        query.offset = mock.Mock(return_value=offset)
        limit = mock.Mock(name='limitTest')
        offset.limit = mock.Mock(return_value=limit)
        limit.all = mock.Mock(return_value=self.testdata)
        filter_by.offset = mock.Mock(return_value=offset)
        filter_by.all = mock.Mock(return_value=self.testdata)

    @property
    def query(self):
        return self.query

    def query_property(self):
        pass

    def __call__(self):
        return self

    def close(self):
        pass

    def rollback(self):
        self.status = 'rollback'

    @query.setter
    def query(self, value):
        self._query = value

    def add(self, model):
        self.instance = model
        self.statusadd = 'add'

    def commit(self):
        self.statuscommit = 'commit'

    def refresh(self, model):
        self.statusrefresh = 'refresh'

    def delete(self, model):
        self.statusdelete = 'delete'


from seismograph.ext.alchemy.registry import *

register_session(FakeSession())

from seismograph.ext.alchemy.orm import *


class TestModelObjects(unittest.TestCase):
    def test_get(self):
        testobject = ModelObjects('testmodel')
        self.assertEqual('testing get', testobject.get(3))

    def test_get_by(self):
        testobject = ModelObjects('testmodel')
        self.assertEqual('testing get_by', testobject.get_by())

    def test_getlist(self):
        testobject = ModelObjects('testmodel')
        self.assertItemsEqual([1, 2, 3, 4], testobject.getlist())

    def test_getlist_by(self):
        testobject = ModelObjects('testmodel')
        self.assertItemsEqual([1, 2, 3, 4], testobject.getlist_by())

    def test_update_by(self):
        testobject = ModelObjects('testmodel')
        self.assertItemsEqual([1, 2, 3, 4], testobject.update_by({'cat': 'dog'}))
        self.assertEqual('add', get_session().statusadd)
        self.assertEqual('commit', get_session().statuscommit)
        self.assertEqual('refresh', get_session().statusrefresh)
        get_session().statusadd = None
        get_session().statuscommit = None
        get_session().statusdelete = None

    def test_remove_by(self):
        testobject = ModelObjects('testmodel')
        testobject.remove_by()
        self.assertEqual('delete', get_session().statusdelete)
        self.assertEqual('commit', get_session().statuscommit)
        get_session().statusdelete = None
        get_session().statuscommit = None


class TestModelCRUD(unittest.TestCase):
    def test_objects(self):
        testcrud = ModelCRUD()
        self.assertIsInstance(testcrud.objects, ModelObjects)

    def test_update(self):
        testcrud = ModelCRUD()
        testcrud.update()
        self.assertEqual('add', get_session().statusadd)
        self.assertEqual('commit', get_session().statuscommit)
        self.assertEqual('refresh', get_session().statusrefresh)
        get_session().statusadd = None
        get_session().statuscommit = None
        get_session().statusdelete = None

    def test_remove(self):
        testcrud = ModelCRUD()
        testcrud.remove()
        self.assertEqual('delete', get_session().statusdelete)
        self.assertEqual('commit', get_session().statuscommit)
        get_session().statuscommit = None
        get_session().statusdelete = None

    def test_create(self):
        testcrud = ModelCRUD()
        returned =  testcrud.create()
        self.assertEqual('add', get_session().statusadd)
        self.assertEqual('commit', get_session().statuscommit)
        self.assertEqual(get_session().instance, returned)
        get_session().statusadd = None
        get_session().statuscommit = None