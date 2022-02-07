from component.base_page import BasePage
from selenium.webdriver.common.by import By
import allure


class DropDownMenu(BasePage):

    def __init__(self, browser, value, container, name=None, container_with_entity=None):
        super().__init__(browser)
        self.name = name
        self.value = value
        self.container = container
        self.container_with_entity = container_with_entity

    def set_value(self):
        if self.value is not None:
            if self.name is None:
                self.name = 'Неизвестное поле'
            with allure.step(f'заполним {self.name}'):
                input_container = (self.container.value[1] + ' input')
                self.click(input_container)
                self.wait_time()
                elements_in_menu = self.are_presence(self.container_with_entity)
                for element in elements_in_menu:
                    if self.value in element.text:
                        element.click()
                    else:
                        raise AssertionError("Элемент с таким названием не найден")
