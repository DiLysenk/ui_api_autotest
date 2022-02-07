from selenium.webdriver.common.by import By
from component.base_page import BasePage
from enum import Enum
import allure


class CssAdminPage(Enum):
    CATALOG = (By.CSS_SELECTOR, '[data-toggle="collapse"]')
    PRODUCTS = (By.CSS_SELECTOR, '.collapse.in li + li a')
    ADD_NEW = (By.CSS_SELECTOR, '[data-original-title="Add New"]')
    PRODUCT_NAME = (By.CSS_SELECTOR, '[placeholder="Product Name"]')
    META_TAG_TITLE = (By.CSS_SELECTOR, '[placeholder="Meta Tag Title"]')
    MODEL = (By.CSS_SELECTOR, '[placeholder="Model"]')
    SAVE = (By.CSS_SELECTOR, '.fa.fa-save')
    SELECT_PRODUCT = (By.CSS_SELECTOR, '[type="checkbox"]')
    DELETE = (By.CSS_SELECTOR, '.fa.fa-trash-o')
    TABLE = (By.CSS_SELECTOR, '.table.table-bordered.table-hover')
    SUCCESS_DELETE = (By.CSS_SELECTOR, '.alert.alert-success.alert-dismissible')


class AdminPage(BasePage):

    loc = CssAdminPage

    def go_to_Products(self):
        with allure.step('перейти в праздел продукты'):
            self.click(CssAdminPage.CATALOG)
            self.click(CssAdminPage.PRODUCTS)
            return self

    def add_product(self, model):
        with allure.step('Перейти на страницу добавления продукта и заполнить поля'):
            self.click(CssAdminPage.ADD_NEW)
            self.fill_input(CssAdminPage.PRODUCT_NAME, model)
            self.fill_input(CssAdminPage.META_TAG_TITLE, model)
            self.click_element(self.find_by_link_text('Data'))
            self.fill_input(CssAdminPage.MODEL, model)
            self.click(CssAdminPage.SAVE)
            return self

    def select_product(self):
        with allure.step('выбор продукта'):
            self.click_nth_child(self.find_visible(CssAdminPage.TABLE), CssAdminPage.SELECT_PRODUCT, 2)
            return self

    def delete_product(self):
        with allure.step('удалить продукт'):
            self.click(CssAdminPage.DELETE)
            alert = self.browser.switch_to.alert
            alert.accept()
