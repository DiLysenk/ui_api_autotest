from component.base_page import BasePage
from selenium.webdriver.common.by import By


class DropDownMenu(BasePage):

    def __init__(self, browser, value, container):
        super().__init__(browser)
        self.value = value
        self.container = container

    def set_value(self):
        if self.value is not None:
            input_container = (self.container[0], self.container[1] + ' input')
            self.click(input_container)
            self.wait_time()

            elements_in_menu = self.are_presence((By.CSS_SELECTOR, '[class*="__menu-list"] .type__option'))
            for element in elements_in_menu:
                if self.value in element.text:
                    element.click()
                else:
                    raise AssertionError("Элемент с таким названием не найден")
