from models.item import ItemModel
from models.store import StoreModel
from tests.base_test_class import BaseTest
import json

class StoreTest(BaseTest):
    def test_store_create(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test_store")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({"name": "test_store", "items": []},
                                     json.loads(response.data))

    def test_store_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                response = client.post("/store/test_store")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A store with name 'test_store' already exists."},
                                     json.loads(response.data))

    def test_store_delete(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.delete("/store/test_store")

                self.assertEqual(response.status_code,200)
                self.assertIsNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({"message":"Store 'test_store' deleted"},
                                     json.loads(response.data))

    def test_store_find(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code,200)
                self.assertDictEqual({"name":"test_store", "items": []},
                                     json.loads(response.data))
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code,404)
                self.assertDictEqual({"message": f"Store 'test_store' not found"},
                                     json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("item",12.34,1).save_to_db()

                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"name":"test_store",'items':
                                        [{
                                          'name': 'item',
                                          'price': 12.34
                                        }]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                StoreModel("test_store_1").save_to_db()

                response = client.get("/stores")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [
                        {'items': [], 'name': 'test_store'},
                        {'items': [], 'name': 'test_store_1'}
                    ]},
                    json.loads(response.data))

    def test_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                StoreModel("test_store_1").save_to_db()
                ItemModel("test item 1",12.34, 2).save_to_db()
                ItemModel("test item 2", 45.67, 2).save_to_db()


                response = client.get("/stores")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [
                        {'items': [], 'name': 'test_store'},
                        {'items': [
                            {'name': 'test item 1', 'price': 12.34},
                            {'name': 'test item 2', 'price': 45.67}
                        ], 'name': 'test_store_1'}
                    ]},
                    json.loads(response.data))