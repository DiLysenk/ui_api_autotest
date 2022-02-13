# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from enum import Enum
import allure

from component.autocomplete_input import AutoCompleteInput
from component.input_field import InputField
from component.drop_down_menu import DropDownMenu
from component.base_page import BasePage
from component.checkbox import CheckBox


class KomTekCSS(Enum):
    FIELD_SEARCH = (By.CSS_SELECTOR, '#search-wrapper-regular')
    INPUT_SELECTOR = (By.CSS_SELECTOR, '.input-text')
    CONTAINER_SEARCH_MENU = (By.CSS_SELECTOR, '.searchautocomplete-placeholder')
    ENTITY_IN_SEARCH_MENU = (By.CSS_SELECTOR, 'li:nth-child(1n)')
    BTN_MAKE_PC = ()
    BTN_CATALOG = ()
    BTN_FOWARD = ()


class KomTekPageObject(BasePage):
    url = 'https://komtek.net.ru/'

    def __init__(self, browser, search_goods=None):
        super().__init__(browser)
        self.search_goods = search_goods

        self.search_goods_attribute = AutoCompleteInput(self.browser, search_goods, KomTekCSS.FIELD_SEARCH,
                                                        name="Поиск товара",
                                                        input_selector=KomTekCSS.INPUT_SELECTOR,
                                                        container_menu=KomTekCSS.CONTAINER_SEARCH_MENU,
                                                        entity_in_menu=KomTekCSS.ENTITY_IN_SEARCH_MENU)
