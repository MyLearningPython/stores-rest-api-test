from models.user import UserModel
from tests.unit.unit_base_test_class import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_user_create(self):
        user = UserModel("test user", "asd")

        self.assertEqual(user.username,"test user",
                         f"Username  {user.username} does not match expected.")
        self.assertEqual(user.password, "asd",
                         f"Password does not matching expected.")