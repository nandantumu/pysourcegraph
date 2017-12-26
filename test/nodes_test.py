"""Test module for nodes.py"""
import unittest
from pysourcegraph import *
from pysourcegraph.parsing import map_folder, map_module

class NodesTest(unittest.TestCase):
    """Test node attributes"""
    def test_base_node_equality(self):
        """Test equality and not equality of BaseNode"""
        self.assertEqual(BaseNode("Test1"), BaseNode("Test1"))
        self.assertEqual(BaseNode("Test1", "docstring here"),
                         BaseNode("Test1", "docstring here"))
        self.assertNotEqual(BaseNode("Test1"), BaseNode("Test2"))
        self.assertNotEqual(BaseNode("Test1", "docstring"),
                            BaseNode("Test1"))

    def test_node_is_childless(self):
        """Test is_childless method of BaseNode"""
        self.assertTrue(BaseNode("Test1").is_childless())
        node = BaseNode("Test1")
        node.add_child(BaseNode("TestChild"))
        self.assertFalse(node.is_childless())

class TreeCreationTest(unittest.TestCase):
    """Test the creation of trees from source"""
    def test_basic_tree_builder(self):
        """Tests that tree_builder returns without error"""
        self.assertIsNotNone(tree_builder(r"C:\Users\nanda\Downloads\astroid-1.6.0"))


if __name__ == '__main__':
    unittest.main()
