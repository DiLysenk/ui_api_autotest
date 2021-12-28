from selenium.webdriver.common.by import By
from pageobject.base_page import BasePage
from enum import Enum
import allure


class AutoPick(BasePage):

    def _set_value_autoinput(self, field, conteiner, text):
        self.click(field)
        self.fill("input" + field, text)
        list_of = self.find_presence(conteiner).find_elements(By.CSS_SELECTOR, 'li')
        for type_content in list_of:
            if type_content.text == text:
                type_content.click()
                break
        else:
            raise AssertionError(f"Не найдено искомое название, {text}")



