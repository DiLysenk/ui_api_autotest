# -*- coding: utf-8 -*-
import logging
import time
from time import sleep
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

CLICK_RETRY = 3




class CssBasePage(Enum):
    LOADING_TAG = (By.CSS_SELECTOR, '.-loading.-active')  # селектор элемента загрузки
    MENU_LINK_TO_CONTENT_PAGE = (By.CSS_SELECTOR, '[href="/new/shows"]')  # кнопка видна из всех разделов


class BasePage:  # базовый класс для PageObject

    def __init__(self, browser, waiting=10):  # инициализация браузера
        self.browser = browser
        self.wait = WebDriverWait(self.browser, waiting)
        self.logger = logging.getLogger(type(self).__name__)

    def __repr__(self):
        return 'base_methods'

    def is_locator(self, locator):
        '''приводит локатор к виду Enum'''
        if isinstance(locator, Enum):
            return locator
        else:
            class NewLocator:
                value = (By.CSS_SELECTOR, locator)
                name = locator
            return NewLocator()

    def is_page_loaded(self):
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')
        self.is_not_visible(CssBasePage.LOADING_TAG)

    def is_visible_by_link_text(self, text):
        """верификация элемента по тексту
        работает если в присутствует атрибут href= в html элемента

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


    def is_visible(self, locator):
        """верификация видимости элемента на странице с помощью локатора

        locator: вида (By, 'locator')
        принимает локатор, возвращает WebElement
        """
        for i in range(CLICK_RETRY, 0, -1):
            try:
                self.is_page_loaded()
                element = self.wait.until(EC.visibility_of_element_located(locator.value))
                self.logger.info(f'успешно найден элемент по локатору с локатором {locator.name}')
                return element
            except TimeoutException:
                sleep(i)
                if i == CLICK_RETRY - 1:
                    self.logger.error(f'ошибка, не найден элемент по css {locator.name}')
                    raise AssertionError(f'ошибка, не найден элемент по css  {locator.name}')


    def is_presence(self, locator):
        """метод для верификации элемента на странице с помощью селектора
        (элемент может быть невидим на странице но он присутствует в DOM)"""
        try:
            locator = self.is_locator(locator)
            self.is_page_loaded()
            element = self.wait.until(EC.presence_of_element_located(locator.value))
            self.logger.info(f'успешно найден элемент по локатору с локатором {locator.name}')

            return element
        except TimeoutException:
            self.logger.error(f'ошибка, не найден элемент по css  {locator.name}')
            raise AssertionError(f'ошибка,не найден элемент по css  {locator.name}')

    def is_visible_by_text(self, text: str):
        """метод для верификации элемента по его названию ,
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
        """метод для верификации элементОВ по селектору,
        quantity: это предпологаемое минимальное количество которое он должен найти"""
        try:
            locator = self.is_locator(locator)
            self.is_page_loaded()
            if len(self.wait.until(EC.visibility_of_all_elements_located(locator.value))) >= quantity:
                return self.wait.until(EC.visibility_of_all_elements_located(locator.value))
            else:
                self.wait_time(3)
                return self.wait.until(EC.visibility_of_all_elements_located(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент не найден {locator.name}')
            raise AssertionError(f'Ошибка, элемент не найден {locator.name}')

    def are_presence(self, locator, quantity: int = 1):
        """метод для верификации элементОВ по селектору,
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
            self.logger.error(f'Ошибка, элемент не найден {locator.name}')
            raise AssertionError(f'Ошибка, элемент не найден {locator.name}')

    def is_clickable(self, locator):
        """метод для верификации элемента с помощью CSS на кликабельность"""
        try:
            locator = self.is_locator(locator)
            self.is_page_loaded()
            element = self.wait.until(EC.element_to_be_clickable(locator.value))
            self.logger.info(f'найден кликабельный элемент {locator.name}')
            return element
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент не кликабельный {locator.name}')
            raise AssertionError(f'Ошибка, элемент не кликабельный {locator.name}')

    def is_not_visible(self, locator):
        try:
            locator = self.is_locator(locator)
            return self.wait.until(EC.invisibility_of_element(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент найден и не исчезает {locator.name}')
            raise AssertionError(f'Ошибка, элемент не исчез с экрана {locator.name}')

    def verify_url(self, url):
        try:
            return self.wait.until(EC.url_to_be(url))
        except TimeoutException:
            self.logger.error(f'Ошибка, адрес странички не  {url}')
            raise AssertionError(f'Ошибка, адрес странички не  {url}')

    def click_element_ac(self, element):
        """клик с помощью экшон чейнс"""
        ActionChains(self.browser).pause(0.1).move_to_element(element).click().perform()

    def click_element(self, element):
        """ Кликает по элементу

        element: WebElement
        принимает WebElement, кликает по WebElement
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

    def click_locator(self, locator):
        """ Кликает по элементу

        locator: вида (By, 'locator')
        принимает WebElement, кликает по WebElement
        """
        for i in range(CLICK_RETRY, 0, -1):
            try:
                self.wait.until(EC.element_to_be_clickable(locator.value)).click()
                self.logger.info(f'клик по элементу c локатором {locator.name}')
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                sleep(i)
                if i == CLICK_RETRY - 1:
                    raise AssertionError(f'Ошибка, не кликнуть по элементу с локатором {locator.name}')


    def click_nth_child(self, element, locator, index: int = 0):
        """ в найденном элементе (например таблице) находит элементы с одинаковым css_selector
         и кликает по порядковому номеру (index) """
        locator = self.is_locator(locator)
        element_child = element.find_elements(*locator.value)[index]
        self.click_element(element_child)
        self.logger.info(f'Клик в элемент по счёту {index} с локатором {locator.name}')
        return self

    def fill(self, locator, text):
        """ввод в поле текста, после очистки его """
        for i in range(CLICK_RETRY):
            try:
                locator = self.is_locator(locator)
                self.scroll_to_element(self.is_visible(locator))
                self.is_visible(locator).clear()
                self.is_visible(locator).send_keys(text)
                self.logger.info(f'заполняем поле текстом -- {text}')
                return self
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise AssertionError(f'Ошибка, не найден элемент, {locator.name}')

    def clear_and_send_keys(self, element, text):
        """ввод в поле текста, после очистки его """
        element.clear()
        element.send_keys(text)
        self.logger.info(f'заполняем поле текстом -- {text}')
        return self


    def send_keys_with_enter(self, element, text):
        """ввод в поле текста и последующее нажатие ENTER
        Подходит для полей фильтров с выпадающем списком"""
        element.send_keys(text)
        element.send_keys(Keys.ENTER)
        self.logger.info(f'заполняем поле текстом -- {text} и нажимаем Enter')
        return self

    def get_attribute_element(self, element, attribute):
        return element.get_attribute(attribute)

    def refresh_browser(self):
        self.browser.refresh()
        self.is_page_loaded()
        return self

    def get_propety_text_of_element(self, element):
        return element.get_property('textContent')

    def get_text_of_element(self, locator):
        locator = self.is_locator(locator)
        return self.is_visible(locator.value).text

    def get_text_of_element_by_text_link(self, text_link):
        return self.is_visible_by_link_text(text_link).text

    def get_html_of_element(self, element):
        return element.get_property('outerHTML')

    def wait_time(self, time: int = 1):
        sleep(time)
        return self

    def click_by_link_text(self, linktext: str):
        self.click_element(self.is_visible_by_link_text(linktext))
        self.is_not_visible(CssBasePage.LOADING_TAG.value)
        return self

    def open_page_by_url(self, url):
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
