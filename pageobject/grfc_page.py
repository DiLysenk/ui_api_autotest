from pageobject.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum


class CssGRFC(Enum):

    BTN_FIND = (By.CSS_SELECTOR, '.top-search-r .search-button')

    FIELD_FIND = (By.CSS_SELECTOR, '#search-line')


class GRFC(BasePage):
    url = 'https://www.grfc.ru/grfc/'

    def open_page(self):
        self.open_page_by_url(self.url)

    def click_find(self):
        self.click_element(self.is_visible(CssGRFC.BTN_FIND))

    def input_in_find(self, text):
        self.clear_and_send_keys(self.is_visible(CssGRFC.FIELD_FIND), text)

    def push_enter(self):
        self.is_visible(CssGRFC.FIELD_FIND).send_keys('Enter')
