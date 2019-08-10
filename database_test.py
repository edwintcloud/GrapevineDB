import unittest
from database import Database
from collection import Collection
from node import Node
import os


class DatabaseTest(unittest.TestCase):
    def test_create_database(self):
        Database()
        self.assertTrue(os.path.exists('data/collections.p'))
        self.assertTrue(os.path.exists('data/nodes.p'))

    def test_wipe_database(self):
        d = Database()
        d.wipe()
        d.insert({"test": "data"})
        d.wipe()
        self.assertEqual(d.num_nodes, 0)

    def test_migrate(self):
        d = Database()
        d.wipe()
        d.migrate("migrations/test_migration.json")
        self.assertEqual(d.num_nodes, 6)
        self.assertEqual(d.num_associations, 8)
        d.wipe()

    def test_add_collection(self):
        d = Database()
        d.wipe()
        col = d.add("test")
        self.assertIn("test", d.collections)
        self.assertIsInstance(col, Collection)
        self.assertRaisesRegex(Exception, "already exists", d.add, "test")
        self.assertRaisesRegex(Exception, "of type str", d.add, 1)
        self.assertRaisesRegex(Exception, "at least 3 characters", d.add, "s")
        d.wipe()

    def test_remove_collection(self):
        d = Database()
        d.wipe()
        d.add("test")
        self.assertEqual(len(d.collections), 1)
        d.remove("test")
        self.assertEqual(len(d.collections), 0)
        self.assertRaisesRegex(
            Exception,
            "not a node or collection in this database",
            d.remove,
            "tsaw",
        )
        d.wipe()

    def test_insert_node(self):
        d = Database()
        d.wipe()
        n = d.insert({"test": "test"}, key="test")
        self.assertIsInstance(n, Node)
        self.assertEqual(d.num_nodes, 1)
        self.assertRaisesRegex(
            Exception, "already exists", d.insert, {"n": "w"}, key="test"
        )
        self.assertRaisesRegex(
            Exception, "must be of type dict", d.insert, "blah"
        )
        d.wipe()

    def test_insert_node_into_collection(self):
        d = Database()
        d.wipe()
        col = d.add("users")
        n = col.insert({"name": "joe"}, key="test")
        self.assertIsInstance(n, Node)
        self.assertEqual(d.num_nodes, 1)
        self.assertRaisesRegex(
            Exception, "already exists", col.insert, {"n": "w"}, key="test"
        )
        self.assertRaisesRegex(
            Exception, "must be of type dict", col.insert, "blah"
        )
        d.wipe()

    def test_relate_to(self):
        pass

    def test_related_by(self):
        pass

    def test_related_difference(self):
        pass


if __name__ == "__main__":
    unittest.main()
