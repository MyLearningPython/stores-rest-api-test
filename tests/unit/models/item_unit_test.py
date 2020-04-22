from models.item import ItemModel
from tests.unit.unit_base_test_class import UnitBaseTest


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertIsNone(item.store,
                          "The store was present and the expected was for a store nto not have been created.")

    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            item.json(),
            expected,
            f"The JSON export of the item is incorrect. Received {item.json()}, expected {expected}.")
