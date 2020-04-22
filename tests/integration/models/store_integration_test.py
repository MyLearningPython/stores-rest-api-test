from models.item import ItemModel
from models.store import StoreModel
from tests.base_test_class import BaseTest


class StoreIntegrationTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("test")

        self.assertListEqual(store.items.all(),[],
                             "Store contains items but the expected was a store without any items linked to it.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel("test")

            self.assertIsNone(store.find_by_name("test"),
                              f"Found store with name <{store.name}> in DB. expected was no store created as no save was done to DB")

            store.save_to_db()

            self.assertIsNotNone(store.find_by_name("test"),
                                 f"No store found with name <{store.name}> in the DB. Expected to find the store after DB save")

            store.delete_from_db()

            self.assertIsNone(store.find_by_name("test"),
                              f"Test found by name {store.name} even the expected was none as the DB was deleted.")



    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("test")
            item = ItemModel("test item",12.34,1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(),1,
                             "There is no store/more than one stores saved in DB. Check that the DB is cleaned and store creation.")
            self.assertEqual(store.items.first().name,"test item",
                             f"The item name linked to the store does not match expected <{item.name}>")


    def test_store_json(self):
        store = StoreModel("test store")
        expected = {
            "id": None,
            "name": "test store",
            "items": [],
        }

        self.assertDictEqual(store.json(),expected)

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel("test store")
            item = ItemModel("test item", 12.34, 1)
            expected = {
                "id": 1,
                "name" : "test store",
                "items" : [{"name" : "test item", "price" : 12.34}],
            }

            store.save_to_db()
            item.save_to_db()

            self.assertDictEqual(store.json(),expected)

    def test_store_save_to_db(self):
        pass

