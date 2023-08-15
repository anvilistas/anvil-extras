"""This is a test module."""
import unittest
import anvil.server
import time

class TestClass(unittest.TestCase):
    """This is a testclass"""

    def test_method_1(self):
        """Test Method 1."""
        pass

    def test_method_2(self):
        """Test Method 2"""
        pass

    def test_method_fail(self):
        """Test that will fail."""
        assert(False)

    def test_method_final(self):
        """Final passing test."""
        pass
        