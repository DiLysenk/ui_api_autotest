# -*- coding: utf-8 -*-
import dataclasses

from selenium.webdriver.common.by import By
from enum import Enum
import allure
from dataclasses import dataclass
from component.autocomplete_input import AutoCompleteInput
from component.search_entity import SearchBy
from component.input_field import InputField
from component.drop_down_menu import DropDownMenu
from component.base_page import BasePage
from component.checkbox import CheckBox


class KomTekCSS(Enum):
    FIELD_SEARCH = (By.CSS_SELECTOR, '#search-wrapper-regular')
    INPUT_SELECTOR = (By.CSS_SELECTOR, '.input-text')
    CONTAINER_SEARCH_MENU = (By.CSS_SELECTOR, '.searchautocomplete-placeholder')
    ENTITY_IN_SEARCH_MENU = (By.CSS_SELECTOR, 'li:nth-child(1n)')
    BTN_NOTEBOOKS = (By.CSS_SELECTOR, '.banner.hotcategory')
    FIELD_PAGINATION = (By.CSS_SELECTOR, '.category-products > div.toolbar > div.sorter > div.limiter > div')
    FIELD_PAGINATION_MENU = (By.CSS_SELECTOR, '.category-products > div.toolbar > div.sorter > div.limiter > div > div')
    ENTITY_IN_PAGINATION_MENU = (By.CSS_SELECTOR, ' li.active-result')

    BTN_FILTER_MANUFACTOR = (By.CSS_SELECTOR, '.new.odd:nth-child(5)')
    CHECKBOX_FILTER_MANUFACTOR = (By.CSS_SELECTOR, '')


@dataclass
class ModelInput:
    search_goods = None
    pagination = None
    filter_manufactor = None


class KomTekPageObject(BasePage, ModelInput):
    url = 'https://komtek.net.ru/'


    def __init__(self, browser):
        super().__init__(browser)
        self.search_goods_attribute = SearchBy(self.browser, self.search_goods, KomTekCSS.FIELD_SEARCH,
                                               name="Поиск товара",
                                               input_selector=KomTekCSS.INPUT_SELECTOR,
                                               container_menu=KomTekCSS.CONTAINER_SEARCH_MENU,
                                               entity_in_menu=KomTekCSS.ENTITY_IN_SEARCH_MENU)

        self.pagination_attribute = DropDownMenu(self.browser, self.pagination, KomTekCSS.FIELD_PAGINATION,
                                                 container_with_entity=KomTekCSS.FIELD_PAGINATION_MENU,
                                                 entity_in_menu=KomTekCSS.ENTITY_IN_PAGINATION_MENU)

        self.filter_manufactor_attribute = CheckBox(self.browser, self.filter_manufactor,
                                                    KomTekCSS.CHECKBOX_FILTER_MANUFACTOR)

    def navigate_to_note_book_table(self):
        self.open_url(self.url)
        self.click_locator(KomTekCSS.BTN_NOTEBOOKS)
