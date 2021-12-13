# -*- coding: utf-8 -*-
import enum
import logging
from time import sleep
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

CLICK_RETRY = 2


class CssBasePage(Enum):
    LOADING_TAG = (By.CSS_SELECTOR, '.-loading.-active')  # селектор элемента загрузки
    MENU_LINK_TO_CONTENT_PAGE = (By.CSS_SELECTOR, '[href="/new/shows"]')  # кнопка видна из всех разделов


class BasePage:  # базовый класс PageObject

    def __init__(self, browser, waiting=10):  # инициализация браузера
        self.browser = browser
        self.wait = WebDriverWait(self.browser, waiting)
        self.logger = logging.getLogger(type(self).__name__)

    def __repr__(self):
        return 'base_methods'

    @staticmethod
    def is_locator(locator):
        """ Приводит локатор к виду Enum """
        if isinstance(locator, Enum):
            return locator
        else:
            class NewLocator(enum.Enum):
                selector = (By.CSS_SELECTOR, locator)

            return NewLocator.selector





    def is_page_loaded(self):
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')

    def click(self, locator):
        """ Клик по элементу
        locator
        принимает локатор, находит веб элемент и клик по нему
        """

        for i in range(CLICK_RETRY, 0, -1):
            try:
                locator = self.is_locator(locator)
                self.find_visible(locator).click()
                self.logger.info(f'клик по элементу c локатором {locator.name}')
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                sleep(i)
                if i == CLICK_RETRY - 1:
                    raise AssertionError(f'Ошибка, не кликнуть по элементу с локатором {locator.name}={locator.value}')

    def click_by_text(self, text):
        """ Клик по элементу
        locator
        принимает локатор, находит веб элемент и клик по нему
        """

        for i in range(CLICK_RETRY, 0, -1):
            try:
                self.find_by_text(text).click()
                self.logger.info(f'клик по элементу c текстом {text}')
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                sleep(i)
                if i == CLICK_RETRY - 1:
                    raise AssertionError(f'Ошибка, не кликнуть по элементу с текстом {text}')




    def fill(self, locator, text):
        """Ввод в поле текста, после очистки его """
        for i in range(CLICK_RETRY):
            try:
                locator = self.is_locator(locator)
                element = self.find_visible(locator)
                self.scroll_to_element(element)
                element.clear()
                element.send_keys(text)
                self.logger.info(f'заполняем поле текстом -- {text}')
                return self
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise AssertionError(f'Ошибка, не найден элемент, {locator.name}={locator.value}')

    def find_presence(self, locator):
        """Метод для верификации элемента на странице с помощью селектора
        (элемент может быть невидим на странице, но он присутствует в DOM)"""
        locator = self.is_locator(locator)
        self.is_page_loaded()
        try:
            element = self.wait.until(EC.presence_of_element_located(locator.value))
            self.logger.info(f'успешно найден элемент по локатору с локатором {locator.name}')
            return element
        except TimeoutException:
            self.logger.error(f'ошибка, не найден элемент  {locator.name}={locator.value}')
            raise AssertionError(f'ошибка,не найден элемент  {locator.name}={locator.value}')

    def find_by_link_text(self, text):
        """Верификация элемента по тексту
        работает если присутствует атрибут href= в html элемента

        text: название элемента
        принимает название, возвращает WebElement
        """
        for i in range(CLICK_RETRY, 0, -1):
            try:
                self.is_page_loaded()
                element = self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, text)))
                self.logger.info(f'успешно найден элемент с текстом -- {text}')
                return element
            except TimeoutException:
                sleep(i)
                if i == CLICK_RETRY - 1:
                    self.logger.error(f'Ошибка, не найдена ссылка с текстом "{text}')
                    raise AssertionError(f'Ошибка, не найдена ссылка с текстом "{text}')

    def find_visible(self, locator):
        """Верификация видимости элемента на странице с помощью локатора

        locator: вида (By, 'locator')
        принимает локатор, возвращает WebElement
        """
        locator = self.is_locator(locator)
        for i in range(CLICK_RETRY, 0, -1):
            try:
                self.is_page_loaded()
                element = self.wait.until(EC.visibility_of_element_located(locator.value))
                self.logger.info(f'успешно найден элемент с локатором {locator.name}={locator.value}')
                return element
            except TimeoutException:
                sleep(i)
                if i == CLICK_RETRY - 1:
                    self.logger.error(f'ошибка, не найден элемент {locator.name}={locator.value}')
                    raise AssertionError(f'ошибка, не найден элемент {locator.name}={locator.value}')






    def are_presence(self, locator, quantity: int = 1):
        """Метод для верификации элементОВ по селектору,
        quantity: это предполагаемое минимальное количество которое он должен найти"""
        try:
            locator = self.is_locator(locator)
            self.is_page_loaded()
            if len(self.wait.until(EC.presence_of_all_elements_located(locator.value))) >= quantity:
                return self.wait.until(EC.presence_of_all_elements_located(locator.value))
            else:
                self.wait_time(3)
                return self.wait.until(EC.presence_of_all_elements_located(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент не найден {locator.name}={locator.value}')
            raise AssertionError(f'Ошибка, элемент не найден {locator.name}={locator.value}')

    def find_by_text(self, text: str):
        """Метод для верификации элемента по его названию,
        для нахождения элемента достаточно указать название элемента"""
        try:
            self.is_page_loaded()
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[text()="{text}"]')))
            self.logger.info(f'найден элемент с текстом {text}')
            return element
        except TimeoutException:
            self.logger.error(f'Ошибка,  не найден элемент с названием {text}')
            raise AssertionError(f'Ошибка, не найден элемент с названием {text}')

    # метод для верификации элементов с помощью локатора
    def are_visible(self, locator, quantity: int = 1):
        """Метод для верификации элементОВ по селектору,
        quantity: это предполагаемое минимальное количество которое он должен найти"""
        try:
            locator = self.is_locator(locator)
            self.is_page_loaded()
            if len(self.wait.until(EC.visibility_of_all_elements_located(locator.value))) >= quantity:
                return self.wait.until(EC.visibility_of_all_elements_located(locator.value))
            else:
                self.wait_time(3)
                return self.wait.until(EC.visibility_of_all_elements_located(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент не найден {locator.name}={locator.value}')
            raise AssertionError(f'Ошибка, элемент не найден {locator.name}={locator.value}')

    def is_not_visible(self, locator):
        try:
            locator = self.is_locator(locator)
            return self.wait.until(EC.invisibility_of_element(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент найден и не исчезает {locator.name}={locator.value}')
            raise AssertionError(f'Ошибка, элемент не исчез с экрана {locator.name}={locator.value}')

    def verify_url(self, url):
        try:
            return self.wait.until(EC.url_to_be(url))
        except TimeoutException:
            self.logger.error(f'Ошибка, адрес странички не  {url}')
            raise AssertionError(f'Ошибка, адрес странички не  {url}')

    def click_element_ac(self, element):
        """Клик с помощью action chains"""
        ActionChains(self.browser).pause(0.1).move_to_element(element).click().perform()

    def click_element(self, element):
        """ Клик по элементу

        element: WebElement
        принимает WebElement, клик по WebElement
        """
        for i in range(CLICK_RETRY, 0, -1):
            try:
                element.click()
                self.logger.info('клик по элементу')
                break
            except (StaleElementReferenceException, ElementClickInterceptedException):
                sleep(i)
                if i == CLICK_RETRY - 1:
                    raise AssertionError('Ошибка, не кликнуть по элементу')

    def click_nth_child(self, element, locator, index: int = 0):
        """ В найденном элементе (например таблице) находит элементы с одинаковым css_selector
         и клик по порядковому номеру (index) """
        locator = self.is_locator(locator)
        element_child = element.find_elements(*locator.value)[index]
        self.click_element(element_child)
        self.logger.info(f'Клик в элемент по счёту {index} с локатором {locator.name}={locator.value}')
        return self

    def fill_element(self, element, text):
        """Ввод в поле текста, после очистки его """
        element.clear()
        element.send_keys(text)
        self.logger.info(f'заполняем поле текстом -- {text}')
        return self

    def send_keys_with_enter(self, element, text):
        """Ввод в поле текста и последующее нажатие ENTER
        подходит для полей фильтров с выпадающем списком"""
        element.send_keys(text)
        element.send_keys(Keys.ENTER)
        self.logger.info(f'заполняем поле текстом -- {text} и нажимаем Enter')
        return self

    @staticmethod
    def get_attribute_element(element, attribute):
        return element.get_attribute(attribute)

    def refresh_browser(self):
        self.browser.refresh()
        self.is_page_loaded()
        return self

    @staticmethod
    def get_property_text_of_element(element):
        return element.get_property('textContent')

    def get_text_of_element(self, locator):
        locator = self.is_locator(locator)
        return self.find_visible(locator).text

    def get_text_of_element_by_text_link(self, text_link):
        return self.find_by_link_text(text_link).text

    @staticmethod
    def get_html_of_element(element):
        return element.get_property('outerHTML')

    def wait_time(self, time: int = 1):
        sleep(time)
        return self

    def click_by_link_text(self, link_text: str):
        self.click_element(self.find_by_link_text(link_text))
        self.is_not_visible(CssBasePage.LOADING_TAG.value)
        return self

    def navigate_to(self, url):
        self.browser.get(url)
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')
        self.is_not_visible(CssBasePage.LOADING_TAG)
        return self

    def save_screenshot(self, request):
        test_name = request.node.name
        self.browser.save_screenshot(f'/logs/screen/{self.browser.session_id} + {test_name}.png')

    def back_to_previous_page(self):
        self.browser.back()
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')
        self.is_not_visible(CssBasePage.LOADING_TAG.value)
        return self

    def scroll_page_down(self):
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        return self

    def scroll_page_up(self):
        self.browser.execute_script('window.scrollTo(0, -document.body.scrollHeight);')
        return self

    def scroll_to_element(self, element):
        self.browser.execute_script('arguments[0].scrollIntoView(true);', element)

    def delete_text_in_element(self, element):
        element.send_keys(Keys.CONTROL + Keys.BACKSPACE)
        return self
