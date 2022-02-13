from component.base_page import BasePage
import allure


class DropDownMenu(BasePage):

    def __init__(self, browser, value, container, name=None, container_with_entity=None, entity_in_menu=None):
        super().__init__(browser)
        self.value = value  # значение, которое выбираем
        self.name = name  # Название поля
        self.container = container  # контейнер с полем
        self.container_with_entity = container_with_entity  # контейнер с вариантами
        self.entity_in_menu = entity_in_menu    # варианты в меню

    def set_value(self):
        if self.value is not None:
            with allure.step(f'кликнем по раскрывающемся меню {self.name}'):
                self.click_locator(self.container)
            self.find_visible(self._container_with_entity())
            menu = self.are_visible(locator=(self._container_with_entity(), self._entity_in_menu()))
            for element in menu:
                text_element = element.text
                if self.value == text_element:
                    self.click_element(element)
                    return self
            else:
                raise AssertionError(f"Элемент с таким названием не найден -- {self.value}")

    def _name(self):
        if self.name is None:
            return 'Неизвестное поле (Имя не указано)'
        else:
            return self.name

    def _entity_in_menu(self):
        if self.entity_in_menu is None:
            return self._is_locator('')
        else:
            return self.entity_in_menu

    def _container_with_entity(self):
        if self.container_with_entity is None:
            return self.container
        else:
            return self.container_with_entity
