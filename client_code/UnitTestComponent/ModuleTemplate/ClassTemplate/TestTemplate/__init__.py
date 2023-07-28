from ._anvil_designer import TestTemplateTemplate
import anvil


class TestTemplate(TestTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.cp_module = anvil.ColumnPanel(role=self.item['card_role'])
        self.fp_runs = anvil.FlowPanel(align='left')
        self.btn_run = anvil.Button(role=self.item['btn_role'], text=self.item['name'])
        self.lbl_success = anvil.Label(icon='fa:check-circle', foreground='#4f7a28',
                                       visible=False, font_size=self.item['check_size'])
        
        self.fp_runs.add_component(self.btn_run)
        self.fp_runs.add_component(self.lbl_success)
        self.cp_module.add_component(self.fp_runs)
        self.add_component(self.cp_module)

        self.btn_run.set_event_handler('click', self.btn_run_test_click)

    def btn_run_test_click(self, **event_args):
        """This method is called when the button is clicked"""
        with anvil.Notification("Test " + self.item['name'] + ' running...'):
            print(self.item['ref'])
            self.item['ref']()
            print('Test ' + self.item['name'] + ' was a success!')
            self.lbl_success.visible = True