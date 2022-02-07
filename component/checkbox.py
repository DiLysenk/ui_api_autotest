from component.base_page import BasePage


class CheckBox(BasePage):

    def __init__(self, browser, value, container):
        super().__init__(browser)
        self.value = value
        self.container = container

    def set_value(self):
        if self.value is not None:
            self.click(self.container)
