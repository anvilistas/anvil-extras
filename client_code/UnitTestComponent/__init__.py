from ._anvil_designer import UnitTestComponentTemplate
import anvil
import unittest


class UnitTestComponent(UnitTestComponentTemplate):
    def __init__(self, test_modules, configs, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.test_modules = test_modules
        self.lbl_test_title.role = configs['title_role']
        self.btn_all_tests.role = configs['btn_role']

        self.test_config = []
        mod_cnt = 0
        for mod in self.test_modules:
            module_ref = self.test_modules[mod]
            classlist = self.get_test_classes(module_ref)
            self.test_config.append(
                {'name': 'Module: ' + mod, 'ref': module_ref, 'children': [],
                 'card_role': configs['card_roles'][0], 'btn_role': configs['btn_role'],
                 'check_size': configs['check_size']}
            )
            
            for testclass in classlist:
                testclass_ref = getattr(module_ref, testclass)
                methods_in_class = dir(testclass_ref)
                methods_list = [
                    {
                        'name': 'Method: ' + am, 'ref': getattr(testclass_ref(), am),
                        'card_role': configs['card_roles'][2], 'btn_role': configs['btn_role'],
                        'check_size': configs['check_size']
                    }
                    for am in methods_in_class if am.startswith('test_')
                ]
                self.test_config[mod_cnt]['children'].append(
                    {
                        'name': 'Class: ' + testclass, 'ref': testclass_ref, 'children': methods_list,
                        'card_role': configs['card_roles'][1], 'btn_role': configs['btn_role'],
                        'check_size': configs['check_size']}
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
        with anvil.Notification("All tests running..."):
            for mod in self.test_config:
                for testclass in mod['children']:
                    tc = testclass['ref']()
                    tc.main()
            print('All tests were a success!')
            self.lbl_success.visible = True