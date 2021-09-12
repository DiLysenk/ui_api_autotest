# -*- coding: utf-8 -*-
import logging
from time import sleep
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class BasePage:  # базовый класс для PageObject

    def __init__(self, browser, wait=10):  # инициализация браузера
        self.browser = browser
        self.wait = WebDriverWait(self.browser, wait)
        self.logger = logging.getLogger(type(self).__name__)

    def verify_page_loaded(self):
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')

    def verify_selected_element(self, element):
        """метод для проверки -выделен ли элемент? на странице  """
        if 'selected' not in element.get_attribute("class"):
            raise AssertionError("неудача, Элемент не был выделен в таблице ")
        else:
            return True

    def verify_link_text_visible(self, link_text):
        """метод для верификации элемента в котором содержиться ссылка для перехода (за это отвечает аттрибут href=)
        для нахождения элемента достаточно указать название элемента"""
        try:
            self.verify_page_loaded()
            element = self.wait.until(ec.visibility_of_element_located((By.LINK_TEXT, link_text)))
            self.logger.info(f'успешно найден элемент с текстом -- {link_text}')
            return element
        except TimeoutException:
            self.logger.error(f'ошибка, элемент с ссылкой по тексту -- {link_text} не найден')
            raise AssertionError(f'Не найти элемент с тексту -- {link_text}')

    def verify_element_visible(self, locator: tuple):
        """метод для верификации "видимого" элемента на странице с помощью селектора"""
        try:
            self.verify_page_loaded()
            element = self.wait.until(ec.visibility_of_element_located(locator))
            self.logger.info(f'успешно найден элемент по локатору с локатором {locator}')
            return element
        except TimeoutException:
            self.logger.error(f'ошибка, элемент по css не найден {locator}')
            raise AssertionError(f'не найти элемент по локатору: {locator}')

    def verify_element_presence(self, locator: tuple):
        """метод для верификации элемента на странице с помощью селектора
        (элемент может быть невидим на странице но он присутствует в DOM)"""
        try:
            self.verify_page_loaded()
            element = self.wait.until(ec.presence_of_element_located(locator))
            self.logger.info(f'успешно найден элемент по локатору с локатором {locator}')
            return element
        except TimeoutException:
            self.logger.error(f'ошибка, элемент по css не найден {locator}')
            raise AssertionError(f'не найти элемент по локатору: {locator}')

    def verify_element_visible_by_text(self, text: str):
        """метод для верификации элемента по его названию ,
        для нахождения элемента достаточно указать название элемента"""
        try:
            self.verify_page_loaded()
            element = self.wait.until(ec.visibility_of_element_located((By.XPATH, f'//*[text()="{text}"]')))
            self.logger.info(f'найден элемент с текстом {text}')
            return element
        except TimeoutException:
            self.logger.error(f'элемент не найден {text}')
            raise AssertionError(f'не могу найти элемент по тексту: {text}')

    # метод для верификации элементов с помощью локатора
    def verify_elements_visible(self, locator: tuple, quantity: int = 1):
        """метод для верификации элементОВ по селектору,
        quantity: это предпологаемое минимальное количество которое он должен найти"""
        try:
            self.verify_page_loaded()
            if len(self.wait.until(ec.visibility_of_all_elements_located(locator))) >= quantity:
                return self.wait.until(ec.visibility_of_all_elements_located(locator))
            else:
                self.wait_time(3)
                return self.wait.until(ec.visibility_of_all_elements_located(locator))
        except TimeoutException:
            self.logger.error(f'элемент не найден {locator}')
            raise AssertionError(f'не могу найти элементы по локатору: {locator}')

    def verify_element_clickable(self, locator: tuple):
        """метод для верификации элемента с помощью CSS на кликабельность"""
        try:
            self.verify_page_loaded()
            element = self.wait.until(ec.element_to_be_clickable(locator))
            self.logger.info(f'найден элемент с кликабельным локатором {locator}')
            return element
        except TimeoutException:
            self.logger.error(f'элемент не найден {locator}')
            raise AssertionError(f'Элемент не становится кликабельным: {locator}')

    def verify_element_not_visible(self, locator: tuple):
        try:
            return self.wait.until(ec.invisibility_of_element_located(locator))
        except TimeoutException:
            self.logger.error(f'элемент найден и не исчезает {locator}')
            raise AssertionError(f'элемент не исчез с экрана {locator}')

    def verify_url(self, url):
        try:
            return self.wait.until(ec.url_to_be(url))
        except TimeoutException:
            self.logger.error(f'адрес странички не  {url}')
            raise AssertionError(f'некорректный адрес страницчки {url}')

    def click_element_ac(self, element):
        """клик с помощью экшон чейнс"""
        ActionChains(self.browser).pause(0.1).move_to_element(element).click().perform()

    def click_element(self, element):
        try:
            self.wait_time(1)
            element.click()
            self.logger.info('клик по элементу')
        except StaleElementReferenceException:
            self.logger.info('клик_1 по элементу не удачен')
            try:
                self.wait_time(1)
                element.click()
                self.logger.info('клик_2 по элементу')
            except ElementClickInterceptedException:
                raise AssertionError('не кликнуть по элементу')

    def click_inside_element(self, element, locator: tuple, index: int = 0):
        """ в найденом элементе (например таблице) находит элементы с одинаковым css_selector
         и кликает по порядковому номеру (index) """
        element = element.find_elements(*locator)[index]
        self.click_element(element)
        self.logger.info(f'Клик в элемент по счёту {index} с локатором {locator}')
        return self

    def enter_keys(self, element, text):
        """ввод в поле текста, после очистки его """
        element.clear()
        element.send_keys(text)
        self.logger.info(f'заполняем поле текстом -- {text}')
        return self

    def push_enter_after_send_keys(self, element, text):
        """ввод в поле текста и последующее нажатие ENTER
        Подходит для полей фильтров с выпадающем списком"""
        element.send_keys(text)
        element.send_keys(Keys.ENTER)
        self.logger.info(f'заполняем поле текстом -- {text} и нажимаем Enter')
        return self

    def get_attribute_element(self, element, attribute):
        return element.get_attribute(attribute)

    def refresh_browser(self):
        self.wait_time(1)
        self.browser.refresh()
        self.verify_page_loaded()
        self.wait_time(1)
        return self

    def get_propety_text_of_element(self, element):
        return element.get_property('textContent')

    def get_text_of_element(self, locator):
        return self.verify_element_visible(locator).text

    def get_text_of_element_by_text_link(self, text_link):
        return self.verify_link_text_visible(text_link).text

    def get_html_of_element(self, element):
        return element.get_property('outerHTML')

    def wait_time(self, time: int = 1):
        sleep(time)
        return self

    def click_by_linktext(self, linktext: str):
        self.click_element(self.verify_link_text_visible(linktext))
        self.verify_page_loaded()
        return self

    def open_page_by_url(self, url):
        self.browser.get(url)
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')
        self.verify_page_loaded()
        return self

    def getting_screenshot(self, request):
        test_name = request.node.name
        self.browser.save_screenshot(f'././logs/screen/{self.browser.session_id} + {test_name}.png')
        self.browser.save_screenshot(f'../../logs/screen/{self.browser.session_id} + {test_name}.png')

    def back_to_previous_page(self):
        self.browser.back()
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')
        self.verify_page_loaded()
        return self

    def scroll_page_down(self):
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        return self

    def scroll_page_up(self):
        self.browser.execute_script('window.scrollTo(0, -document.body.scrollHeight);')
        return self

    def delete_text_in_element(self, element):
        element.send_keys(Keys.CONTROL + Keys.BACKSPACE)
        return self

    def click_with_selector(self, locator, verify="visible"):
        """ выполняет клик по элменту с дополнительным указанием верификации элемента
        если верификация выполняется по text или link_text, то вместо локатора подставляется текст элемента
        """
        if verify == "visible":
            self.click_element(self.verify_element_visible(locator))
            return self
        elif verify == "presence":
            self.click_element(self.verify_element_presence(locator))
            return self
        elif verify == "text":
            text = locator
            self.click_element(self.verify_element_visible_by_text(text))
            return self
        elif verify == "link_text":
            link_text = locator
            self.click_element(self.verify_link_text_visible(link_text))
            return self
        else:
            raise AssertionError("Ошибка, нужно выбрать метод верификации см. подсказку к методу")

    def enter_keys_with_selector(self, input_text, locator, verify="visible"):
        """ выполняет ввод текста в элмент с дополнительным указанием верификации элемента
        если верификация выполняется по text или link_text, то вместо локатора подставляется текст элемента
        """
        if verify == "visible":
            self.enter_keys(self.verify_element_visible(locator), input_text)
            return self
        elif verify == "presence":
            self.enter_keys(self.verify_element_presence(locator), input_text)
            return self
        elif verify == "text":
            text = locator
            self.enter_keys(self.verify_element_visible_by_text(text), input_text)
            return self
        elif verify == "link_text":
            link_text = locator
            self.enter_keys(self.verify_link_text_visible(link_text), input_text)
            return self
        else:
            raise AssertionError("Ошибка, нужно выбрать метод верификации см. подсказку к методу")
