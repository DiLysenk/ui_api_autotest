from pageobject.base_page import BasePage
from selenium.webdriver.common.by import By
from enum import Enum
from config import settings
from selenium.webdriver.support.ui import Select


class CssTMDB(Enum):
    LOGIN = (By.CSS_SELECTOR, '.primary > li:nth-child(3) a')

    ADMIN = (By.CSS_SELECTOR, '[for="username"] #username')
    PASSWORD = (By.CSS_SELECTOR, '[for="password"] #password')
    BTN_LOGIN = (By.CSS_SELECTOR, '#login_button.k-button')

    ADD_FILM = (By.CSS_SELECTOR, '')
    SEARCH_FIELD = (By.CSS_SELECTOR, '#inner_search_v4')
    SEARCH_BTN = (By.CSS_SELECTOR, '[type="submit"]')


    LOG_SUCCESSFUL = (By.CSS_SELECTOR,)
    FILMS = (By.CSS_SELECTOR, '.content .dropdown_menu > li:nth-child(1)')
    POPULAR = (By.CSS_SELECTOR, '.content .dropdown_menu > li:nth-child(1) li:nth-child(1)')
    SORT_RESULT_BY = (By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(1) > div.filter > span > span')
    SORT_BTN = (By.CSS_SELECTOR, '[name="sort_by"]')

class TMDB(BasePage):
    url = 'https://www.themoviedb.org/'
    
    loc = CssTMDB
    
    def navitage(self):
        self.open_page_by_url(self.url)

    def login(self):
        self.click(CssTMDB.LOGIN)
        self.fill(CssTMDB.ADMIN, settings.tmdb.admin)
        self.fill(CssTMDB.PASSWORD, settings.tmdb.password)
        self.click(CssTMDB.BTN_LOGIN)

    def navigate_to_popular(self):
        self.click(CssTMDB.FILMS)
        self.click(CssTMDB.POPULAR)

    def choose_by(self):
        self.click(CssTMDB.SORT_RESULT_BY)

    def select_element(self, locator, text):
        self.click(CssTMDB.SORT_BTN)
        self.find_by_text()

    def search_movie(self, text):
        self.fill(CssTMDB.SEARCH_FIELD, text)
        self.click('')
        pass
