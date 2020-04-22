from tests.unit.unit_base_test_class import UnitBaseTest
from models.store import StoreModel

class StoreTest(UnitBaseTest):
    def test_store_create(self):
        store = StoreModel("test store 1")

        self.assertEqual(store.name,"test store 1",
                         "Name of the store after creation does not match the expected constructor argument")
