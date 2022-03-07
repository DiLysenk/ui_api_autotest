from component.base_page import BasePage
from component.locators import Locator


class InputField(BasePage):

    def __init__(self, browser, container, input_selector=None):
        super().__init__(browser)
        self.container = container
        self.input_selector = input_selector

    def set_value(self, value):
        if value is not None:
            self.fill_input(self.container, value)


    def _input_field(self):
        if self.input_selector is None:
            return self.container.value[1] + " " + 'input'
        else:
            return Locator.is_locator()
