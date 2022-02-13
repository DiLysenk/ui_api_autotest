from component.base_page import BasePage


class SearchBy(BasePage):

    def __init__(self, browser, value, container):
        super().__init__(browser)
        self.value = value
        self.container = container

    def set_value(self):
        if self.value is not None:
            input_container = (self.container[0], self.container[1] + ' input')
            self.fill_input(input_container, self.value)
            self.wait_time()
            locator_menu = (self.container[0], self.container[1] + ' [class*="__menu-list"]')
            menu = self.are_visible(locator_menu)
            self.wait_time()
            for element in menu:
                if self.value in element.text:
                    self.click_element(element)
                else:
                    raise AssertionError("Элемент с таким названием не найден")