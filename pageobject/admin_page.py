from selenium.webdriver.common.by import By
from pageobject.base_page import BasePage
from enum import Enum


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

    def go_to_Products(self):
        self.click_locator(CssAdminPage.CATALOG)
        self.click_locator(CssAdminPage.PRODUCTS)
        return self

    def add_product(self, model):
        self.click_locator(CssAdminPage.ADD_NEW)
        self.clear_and_send_keys(self.is_visible(CssAdminPage.PRODUCT_NAME), model)
        self.clear_and_send_keys(self.is_visible(CssAdminPage.META_TAG_TITLE), model)
        self.click_element(self.is_visible_by_link_text('Data'))
        self.clear_and_send_keys(self.is_visible(CssAdminPage.MODEL), model)
        self.click_locator(CssAdminPage.SAVE)
        return self

    def select_product(self):
        self.click_nth_child(self.is_visible(CssAdminPage.TABLE), CssAdminPage.SELECT_PRODUCT, 2)
        return self

    def delete_product(self):
        self.click_locator(CssAdminPage.DELETE)
        alert = self.browser.switch_to.alert
        alert.accept()
