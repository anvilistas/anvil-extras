# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# This software is published at https://github.com/anvilistas/anvil-extras

import unittest

import anvil

from ._anvil_designer import UnitTestComponentTemplate

__version__ = "2.4.0"


class UnitTestComponent(UnitTestComponentTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        if not self.card_roles:
            self.card_roles = [None, None, None]

        if not self.test_modules:
            self.test_modules = []

        self.lbl_test_title.role = self.title_role
        self.btn_all_tests.role = self.btn_role

        self.test_config = []
        mod_cnt = 0
        for module_ref in self.test_modules:
            classlist = self.get_test_classes(module_ref)
            self.test_config.append(
                {
                    "name": "Module: " + getattr(module_ref, "__name__").split(".")[-1],
                    "ref": module_ref,
                    "children": [],
                    "card_role": self.card_roles[0],
                    "btn_role": self.btn_role,
                    "icon_size": self.icon_size,
                }
            )

            for testclass in classlist:
                testclass_ref = getattr(module_ref, testclass)
                methods_in_class = dir(testclass_ref)
                methods_list = [
                    {
                        "name": "Method: " + am,
                        "ref": getattr(testclass_ref(), am),
                        "card_role": self.card_roles[2],
                        "btn_role": self.btn_role,
                        "icon_size": self.icon_size,
                    }
                    for am in methods_in_class
                    if am.startswith("test_")
                ]
                self.test_config[mod_cnt]["children"].append(
                    {
                        "name": "Class: " + testclass,
                        "ref": testclass_ref,
                        "children": methods_list,
                        "card_role": self.card_roles[1],
                        "btn_role": self.btn_role,
                        "icon_size": self.icon_size,
                    }
                )

            mod_cnt += 1

        self.rp_modules.items = self.test_config

    def get_test_classes(self, module):
        test_classes = []
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, unittest.TestCase):
                test_classes.append(attribute_name)
        return test_classes

    def btn_all_tests_click(self, **event_args):
        """This method is called when the button is clicked"""
        testmodules = self.rp_modules.get_components()
        for mod in testmodules:
            test_cp = mod.get_components()[0]
            test_fp = test_cp.get_components()[0]
            test_btn = test_fp.get_components()[0]
            test_btn.raise_event("click")
            fail_icon = test_fp.get_components()[3]
            if fail_icon.visible:
                self.lbl_fail.visible = True
        if not self.lbl_fail.visible:
            self.lbl_success.visible = True
