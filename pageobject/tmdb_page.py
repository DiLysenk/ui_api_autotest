import allure

from pageobject.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum


class CssTMDB(Enum):

    LOGIN = (By.CSS_SELECTOR, '.top-search-r .search-button')

    ADMIN = (By.CSS_SELECTOR, '')
    PASSWORD =  (By.CSS_SELECTOR, '')
    BTN_LOGIN =  (By.CSS_SELECTOR, '')

    ADD_FILM = (By.CSS_SELECTOR, '')
    SEARCH_FILM = (By.CSS_SELECTOR, '')

class TMDB(BasePage):

    pass

