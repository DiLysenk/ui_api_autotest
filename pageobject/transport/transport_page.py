from selenium.webdriver.common.by import By
from component.base_page import BasePage
from enum import Enum
import allure
from selenium.webdriver.support.ui import Select


class CssTransportPage(Enum):
    CHOOSE_TRANSPORT = (By.CSS_SELECTOR, '.search_content #transport-type')
    NUMBER_FILED = (By.CSS_SELECTOR, '.search_content .searchcell:nth-child(3) input')
    NAME_STATION = (By.CSS_SELECTOR, '.search_content .searchcell:nth-child(4) input')
    NAME_STREET = (By.CSS_SELECTOR, '.search_content .searchcell:nth-child(5) input')
    BTN_FIND = (By.CSS_SELECTOR, '#search-button.search_go')
    BTN_CLEAR = (By.CSS_SELECTOR, '#clear-filter-button.search_go')


class TransportPage(BasePage):
    URL = 'https://transport.orgp.spb.ru/Portal/transport/main'

    locator = CssTransportPage

    def _check_element(self, element):
        try:
            self.find_visible(element)
        except:
            raise AssertionError('нет поля для страницы главной страницы')

    def navigate(self):
        with allure.step('Открываем экран '):
            self.navigate_to(self.URL)

    def select_transport(self, transport: str):
        select_transport = Select(self.find_visible(self.locator.CHOOSE_TRANSPORT))
        select_transport.select_by_visible_text(transport)
        return self

    def fill_number_field(self, number):
        with allure.step('заполним поле с номером маршрута'):
            self._check_element('div.search')
            self.fill(self.locator.NUMBER_FILED, number)
            return self

    def fill_name_station(self, station):
        with allure.step(f'заполним поле с станции {station}'):
            self._check_element('div.search')
            self.fill(self.locator.NAME_STATION, station)
            return self

    def fill_name_street(self, street):
        with allure.step(f'заполним поле с улицы {street}'):
            self._check_element('div.search')
            self.fill(self.locator.NAME_STREET, street)
            return self

    def press_btn_find(self):
        with allure.step('нажмём кнопку поиск'):
            self._check_element('div.search')
            self.click(self.locator.BTN_FIND)
            return self


