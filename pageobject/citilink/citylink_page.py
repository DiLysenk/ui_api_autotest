# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from enum import Enum
import allure

from component.autocomplete_input import AutoCompleteInput
from component.input_field import InputField
from component.drop_down_menu import DropDownMenu
from component.base_page import BasePage
from component.checkbox import CheckBox


class CityCSS(Enum):
    configurator = (By.CSS_SELECTOR, '.MainMenu__link [data-dy-cevent="top_nav"]')
    search_by_item = (By.CSS_SELECTOR, '.MainH123eader__search .SearchQuickResult__input-wrapper')
    container_search_by_item = (By.CSS_SELECTOR, '.InstantSearch__results')


class CityPO(BasePage):
    url = 'https://www.citilink.ru/'


    def __init__(self, browser, poisk=None):
        super().__init__(browser)
        self.poisk = poisk

        self.poisk_field = AutoCompleteInput(self.browser, poisk,
                                             container=CityCSS.search_by_item,
                                             container_with_entity=CityCSS.container_search_by_item)









