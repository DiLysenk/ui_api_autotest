from component.base_page import BasePage


class CheckBox(BasePage):

    def __init__(self, browser, container):
        super().__init__(browser)
        self.container = container

    def set_value(self, value):
        if value is not None:

            self.click_locator(self.container)
