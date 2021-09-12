from .base_page import BasePage
from selenium.webdriver.common.by import By

class GooglePage(BasePage):
    url_g = 'https://www.google.com/'
    MNE_POVESET = (By.CSS_SELECTOR, '.gNO89b')


