from component.base_page import BasePage
import allure


class DropDownMenu(BasePage):

    def __init__(self, browser, value, container, name=None, container_with_entity=None):
        super().__init__(browser)
        self.value = value
        self.container = container  # контейнер с полем
        self.container_with_entity = container_with_entity  # контейнер с вариантами
        self.name = name  # Название поля
        self.entity_in_menu = '.filters-popup__link-text'
        self.popup = self.container.value

    def _name(self):
        if self.name is None:
            self.name = 'Неизвестное поле (Имя не указано)'

    def _container_with_entity(self):
        if self.container_with_entity is None:
            self.container_with_entity = self.container

    def set_value(self):
        if self.value is not None:
            self._name()
            self._container_with_entity()
            with allure.step(f'кликнем по раскрывающемся меню'):
                try:
                    self.click_locator(self.popup)
                except:
                    raise AssertionError(f'не найдено поле для {self.popup}')
            try:
                self.find_visible(self.container_with_entity)
            except:
                raise AssertionError(f'меню с вариантами выбора не отобразилось {self.container_with_entity}')
            self.wait_time(3)
            menu = self.are_visible(self.container_with_entity.value[1] + " " + self.entity_in_menu)
            for element in menu:
                text_element = element.text
                if self.value == text_element:
                    self.click_element(element)
                    return
                else:
                    raise AssertionError("Элемент с таким названием не найден")


