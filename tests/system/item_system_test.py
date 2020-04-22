from models.store import StoreModel
from models.item import ItemModel
from models.user import UserModel
import json

from tests.base_test_class import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel("test", "1234").save_to_db()
                auth_request = client.post("/auth",
                                           data=json.dumps({"username": "test",
                                                            "password": "1234"
                                                            }),
                                           headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_request.data)["access_token"]
                self.access_token = f"JWT {auth_token}"

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test")

                self.assertEqual(resp.status_code,401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get("/item/test", headers = {"Authorization": self.access_token})
                self.assertEqual(resp.status_code,404)


    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test",12.34,1).save_to_db()
                resp = client.get("/item/test", headers = {"Authorization": self.access_token})
                self.assertEqual(resp.status_code,200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                ItemModel("test",12.34,1).save_to_db()

                resp=client.delete("/item/test")

                self.assertEqual(resp.status_code, 200)
                self.assertEqual({"message": "Item 'test' deleted"},
                                 json.loads(resp.data))
                self.assertIsNone(ItemModel.find_by_name("test"))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()

                resp= client.post("/item/test", data={"price":12.23,"store_id": "1"})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 12.23},json.loads(resp.data))

    def test_create_duplicate(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                client.post("/item/test", data={"price": 12.23, "store_id": "1"})

                resp= client.post("/item/test", data={"price":12.23,"store_id": "1"})

                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(resp.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                resp = client.put("/item/test", data={"price": 12.34, "store_id": "1"})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 12.34}, json.loads(resp.data))



    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                client.post("/item/test", data={"price": 12.23, "store_id": "1"})
                resp = client.put("/item/test", data={"price": 99.99, "store_id": "1"})

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'name': 'test', 'price': 99.99}, json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test").save_to_db()
                client.post("/item/test", data={"price": 12.23, "store_id": "1"})

                resp = client.get("/items")
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'items': [{'name': 'test', 'price': 12.23}]}, json.loads(resp.data))