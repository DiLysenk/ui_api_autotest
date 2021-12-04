import allure

from pageobject.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum


class CssGRFC(Enum):

    BTN_FIND = (By.CSS_SELECTOR, '.top-search-r .search-button')

    FIELD_FIND = (By.CSS_SELECTOR, '#search-line')


class GRFC(BasePage):
    url = 'https://www.grfc.ru/grfc/'

    def open_page(self):
        with allure.step('open page'):
            self.open_page_by_url(self.url)

    def click_find(self):
        with allure.step('click in find'):
            self.click_element(self.find_visible(CssGRFC.BTN_FIND))

    def input_in_find(self, text):
        with allure.step('input at find field'):
            self.fill_element(self.find_visible(CssGRFC.FIELD_FIND), text)

    def push_enter(self):
        with allure.step('push enter'):
            self.find_visible(CssGRFC.FIELD_FIND).send_keys('Enter')



