from .base_page import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    CURRENCY = (By.CSS_SELECTOR, '.btn.btn-link.dropdown-toggle')
    POUND_STERLING = "£ Pound Sterling"
    CABINET = (By.CSS_SELECTOR, '.hidden-xs.hidden-sm.hidden-md')
    OpenCArt = 'http://172.17.0.1:7070'


    def change_currency(self):
        self.click_element(self.verify_element_visible(self.CURRENCY))
        self.click_element(self.verify_element_visible_by_text(self.POUND_STERLING))

    def forward_to_register(self):
        self.click_element(self.verify_element_clickable(self.CABINET))
        self.click_element((self.verify_element_visible_by_text('Регистрация')))
