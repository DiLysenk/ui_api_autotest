import allure

from pageobject.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum
from config import settings


class CssTMDB(Enum):

    LOGIN = (By.CSS_SELECTOR, '.primary > li:nth-child(3) a')

    ADMIN = (By.CSS_SELECTOR, '[for="username"] #username')
    PASSWORD = (By.CSS_SELECTOR, '[for="password"] #password')
    BTN_LOGIN = (By.CSS_SELECTOR, '#login_button.k-button')

    ADD_FILM = (By.CSS_SELECTOR, '')
    SEARCH_FILM = (By.CSS_SELECTOR, '')

    LOG_SUCCESSFUL = (By.CSS_SELECTOR, )
    FILMS = (By.CSS_SELECTOR, '.content .dropdown_menu > li:nth-child(1)')
    POPULAR = (By.CSS_SELECTOR, '.content .dropdown_menu > li:nth-child(1) li:nth-child(1)')


class TMDB(BasePage):

    url = 'https://www.themoviedb.org/'

    def navitage(self):
        self.open_page_by_url(self.url)

    def login(self):
        self.click(CssTMDB.LOGIN)
        self.fill(CssTMDB.ADMIN, settings.tmdb.admin)
        self.fill(CssTMDB.PASSWORD, settings.tmdb.password)
        self.click(CssTMDB.BTN_LOGIN)

    def naviate_to_pop(self):
        self.click(CssTMDB.FILMS)
        self.click(CssTMDB.POPULAR)

    def choose_by(self):
        self.is_visible()
