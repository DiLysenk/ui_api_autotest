from selenium.webdriver.common.by import By
from .base_page import BasePage


class AdminPage(BasePage):
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

    def go_to_Products(self):
        self.click_element(self.verify_element_clickable(self.CATALOG))
        self.click_element(self.verify_element_clickable(self.PRODUCTS))
        return self

    def add_product(self, model):
        self.click_element(self.verify_element_clickable(self.ADD_NEW))
        self.enter_keys(self.verify_element_visible(self.PRODUCT_NAME), model)
        self.enter_keys(self.verify_element_visible(self.META_TAG_TITLE), model)
        self.click_element(self.verify_link_text_visible('Data'))
        self.enter_keys(self.verify_element_visible(self.MODEL), model)
        self.click_element(self.verify_element_clickable(self.SAVE))
        return self

    def select_product(self):
        self.click_inside_element(self.verify_element_visible(self.TABLE), self.SELECT_PRODUCT, 2)
        return self

    def delete_product(self):
        self.click_element(self.verify_element_visible(self.DELETE))
        alert = self.browser.switch_to.alert
        alert.accept()
