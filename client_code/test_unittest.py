# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

__version__ = "2.4.0"

"""This is a test module."""
import unittest


class TestClass(unittest.TestCase):
    """This is a testclass"""

    def test_method_1(self):
        """Test Method 1."""
        assert True

    def test_method_2(self):
        """Test Method 2"""
        pass

    def test_method_fail(self):
        """Test that will fail."""
        assert False

    def test_method_final(self):
        """Final passing test."""
        pass
