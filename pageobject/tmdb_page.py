import ctypes

from pageobject.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum
from config import settings
import allure



class CssTMDB(Enum):
    LOGIN = (By.CSS_SELECTOR, '.primary > li:nth-child(3) a')

    ADMIN = (By.CSS_SELECTOR, '[for="username"] #username')
    PASSWORD = (By.CSS_SELECTOR, '[for="password"] #password')
    BTN_LOGIN = (By.CSS_SELECTOR, '#login_button.k-button')

    ADD_FILM = (By.CSS_SELECTOR, '')
    SEARCH_FIELD = (By.CSS_SELECTOR, '#inner_search_v4')
    SEARCH_BTN = (By.CSS_SELECTOR, '[value="Search"]')

    FILMS = (By.CSS_SELECTOR, '.content .dropdown_menu > li:nth-child(1)')
    POPULAR = (By.CSS_SELECTOR, '.content .dropdown_menu > li:nth-child(1) li:nth-child(1)')
    SORT_RESULT_BY = (By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(1) > div.filter > span > span')
    SORT_BTN = (By.CSS_SELECTOR, '[name="sort_by"]')


class TMDB(BasePage):
    url = 'https://www.themoviedb.org/'

    loc = CssTMDB

    def navigate(self):
        with allure.step(f'перейдём на страницу {self.url}'):
            self.navigate_to(self.url)
            return self

    def login(self):
        with allure.step('Введём логин и пароль'):
            self.click(CssTMDB.LOGIN)
            self.fill(CssTMDB.ADMIN, settings.tmdb.admin)
            self.fill(CssTMDB.PASSWORD, settings.tmdb.password)
            self.click(CssTMDB.BTN_LOGIN)
        return self

    def navigate_to_popular(self):
        with allure.step('перейдём на страницу popular'):
            self.click(CssTMDB.FILMS)
            self.click(CssTMDB.POPULAR)
        return self

    def fill_search_field(self, text):
        with allure.step(f'введём в поиск {text}'):
            self.fill(CssTMDB.SEARCH_FIELD, text)
            self.click(CssTMDB.SEARCH_BTN)
        return self

