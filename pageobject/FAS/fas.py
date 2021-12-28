from selenium.webdriver.common.by import By
from pageobject.base_page import BasePage
from enum import Enum
import allure
from selenium.webdriver.support.ui import Select


class CssFAS(Enum):
    pass


class PageFAS:


    URL = 'https://br.fas.gov.ru/?divisions=a026fa29-876d-4340-9da3-ba34db7a4cf6&type=1&order_by=reg_date&direction=desc'

    locator = CssFAS


