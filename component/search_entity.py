from component.base_page import BasePage
from component.locators import Locator
import allure


class SearchBy(BasePage):

    def __init__(self, browser, container,
                 name=None,
                 input_selector=None,
                 container_menu=None,
                 entity_in_menu=None):
        super().__init__(browser)
        self.container = container  # контейнер с полем
        self.input_selector = input_selector
        self.container_menu = container_menu  # контейнер с вариантами
        self.name = name  # Название поля
        self.entity_in_menu = entity_in_menu

    def set_value(self, value):
        if value is not None:
            self._name()
            self._entity_in_menu()
            with allure.step(f'заполним поле {self._name()} значением {value}'):
                self.fill_input(self._input_field(), value)
            self.find_visible(self._container_menu())
            menu = self.are_visible(locator=(self._container_menu(), self._entity_in_menu()))
            for element in menu:
                if value in element.text:
                    self.click_element(element)
                    return self
            else:
                raise AssertionError("Элемент с таким названием не найден")

    def _name(self):
        if self.name is None:
            return 'Неизвестное поле (Имя не указано)'

    def _entity_in_menu(self):
        if self.entity_in_menu is None:
            return Locator.is_locator('')
        else:
            return self.entity_in_menu

    def _input_field(self):
        if self.input_selector is None:
            return self.container.value[1] + " " + 'input'
        else:
            return self.container.value[1] + " " + self.input_selector.value[1]

    def _container_menu(self):
        if self.container_menu is not None:
            return self.container_menu
