from models.user import UserModel
from tests.base_test_class import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("test_user", "asd")

            self.assertIsNone(UserModel.find_by_username("test_user"),
                              f"User found by name <{user.username}> in DB when expected was None. ")
            self.assertIsNone(UserModel.find_by_id(1),
                              "User found by id 1 in DB when expected was None.")

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username("test_user"),
                              f"User not found by name <{user.username}> in DB when expected was to find it. ")
            self.assertIsNotNone(UserModel.find_by_id(1),
                              "User not found by id 1 in DB when expected was returned user by id.")


