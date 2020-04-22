from models.user import UserModel
from tests.base_test_class import BaseTest
import json

class UserTest(BaseTest):
    def test_user_register(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register",
                                data={'username': "test", "password": "asd"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("test"))
                self.assertDictEqual({"message": "User was created successfully."},
                                    json.loads(response.data))

    def test_user_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={'username': "test", "password": "asd"})
                auth_response = client.post("/auth",
                                    data=json.dumps({'username': "test", "password": "asd"}),
                                    headers={"Content-Type": "application/json"})

                self.assertIn("access_token", json.loads(auth_response.data).keys())


    def test_user_duplicate(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={'username': "test", "password": "asd"})
                response = client.post("/register", data={'username': "test", "password": "asd"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with the username already exists."},
                                     json.loads(response.data))

