# -*- coding: utf-8 -*-
from component.locators import Locator
import logging
from time import sleep
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, \
    ElementClickInterceptedException, ElementNotInteractableException
from enum import Enum
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import allure
from typing import Union

RETRY = 2


class CssBasePage(Enum):
    LOADING_TAG = (By.CSS_SELECTOR, '.-loading.-active')  # селектор элемента загрузки
    MENU_LINK_TO_CONTENT_PAGE = (By.CSS_SELECTOR, '[href="/new/shows"]')  # кнопка видна из всех разделов


class BasePage:  # базовый класс PageObject

    def __init__(self, browser, waiting=10):  # инициализация браузера
        self.browser = browser
        self.wait = WebDriverWait(self.browser, waiting)
        self.logger = logging.getLogger(type(self).__name__)

    def is_page_loaded(self):
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')

    def click_locator(self, locator):
        """ Клик по элементу
        locator
        принимает локатор, находит веб элемент и клик по нему
        """
        for i in range(RETRY, 0, -1):
            try:
                locator = self._is_locator(locator)
                element = self.find_presence(locator)
                sleep(i * 0.5)
                self.move_to_element(element)
                self.click_element(element)
                self.logger.info(f'клик по элементу c локатором {locator.name}')
                return self
            except (StaleElementReferenceException, ElementClickInterceptedException):
                if i == 1:
                    raise AssertionError(f'Ошибка, не кликнуть по элементу с локатором {locator.name}={locator.value}')

    @allure.step('Клик c текстом {text}')
    def click_by_text(self, text):
        """ Клик по элементу
        locator
        принимает локатор, находит веб элемент и клик по нему
        """

        for i in range(RETRY, 0, -1):
            try:
                self.find_by_text(text).click()
                self.logger.info(f'клик по элементу c текстом {text}')
                return self
            except (StaleElementReferenceException, ElementClickInterceptedException):
                sleep(i)
                if i == 1:
                    raise AssertionError(f'Ошибка, не кликнуть по элементу с текстом {text}')

    @allure.step('Заполним {locator} c текстом {text}')
    def fill_input(self, locator: [Enum, str], text):
        """Ввод в поле текста, после очистки его """
        for i in range(RETRY):
            try:
                locator = self._is_locator(locator)
                element = self.find_presence(locator)
                # element.clear()
                element.send_keys(text)
                self.logger.info(f'заполняем поле текстом -- {text}')
                return self
            except (StaleElementReferenceException, ElementNotInteractableException):
                if i == 1:
                    raise AssertionError(f'Ошибка, не найден элемент, {locator.name}={locator.value}')

    def find_presence(self, locator):
        """Метод для верификации элемента на странице с помощью селектора
        (элемент может быть невидим на странице, но он присутствует в DOM)"""
        locator = self._is_locator(locator)
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
        for i in range(RETRY, 0, -1):
            try:
                self.is_page_loaded()
                element = self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, text)))
                self.logger.info(f'успешно найден элемент с текстом -- {text}')
                return element
            except TimeoutException:
                sleep(i)
                if i == 1:
                    self.logger.error(f'Ошибка, не найдена ссылка с текстом "{text}')
                    raise AssertionError(f'Ошибка, не найдена ссылка с текстом "{text}')

    @allure.step('Заполним')
    def find_visible(self, locator):
        """Верификация видимости элемента на странице с помощью локатора

        locator: вида (By, 'locator')
        принимает локатор, возвращает WebElement
        """
        locator = self._is_locator(locator)
        for i in range(RETRY, 0, -1):
            try:
                self.is_page_loaded()
                element = self.wait.until(EC.visibility_of_element_located(locator.value))
                self.logger.info(f'успешно найден элемент с локатором {locator.name}={locator.value}')
                return element
            except TimeoutException:
                sleep(i)
                if i == 1:
                    self.logger.error(f'ошибка, не найден элемент {locator.name}={locator.value}')
                    raise AssertionError(f'ошибка, не найден элемент {locator.name}={locator.value}')

    def are_presence(self, locator, quantity: int = 1):
        """Метод для верификации элементОВ по селектору,
        quantity: это предполагаемое минимальное количество которое он должен найти"""
        try:
            locator = self._is_locator(locator)
            self.is_page_loaded()
            if len(self.wait.until(EC.presence_of_all_elements_located(locator.value))) >= quantity:
                return self.wait.until(EC.presence_of_all_elements_located(locator.value))
            else:
                self.wait_time(3)
                return self.wait.until(EC.presence_of_all_elements_located(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент не найден {locator.name}={locator.value}')
            raise AssertionError(f'Ошибка, элемент не найден {locator.name}={locator.value}')

    def find_by_text(self, text: str, locator: (str, None) = None):
        """Метод для верификации элемента по его названию,
        для нахождения элемента достаточно указать название элемента"""
        self.is_page_loaded()
        if locator is None:
            xpath_locator = f'//*[text()="{text}"]'
        else:
            xpath_locator = Locator.to_xpath(locator, text)
        try:
            element = self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_locator)))
            self.logger.info(f'найден элемент с текстом {text}')
            return element
        except TimeoutException:
            self.logger.error(f'Ошибка,  не найден элемент -- {xpath_locator} -- с названием -- {text}')
            raise AssertionError(f'Ошибка, не найден элемент -- {xpath_locator} -- с названием -- {text}')

    # метод для верификации элементов с помощью локатора
    def are_visible(self, locator: Union[Enum, str, tuple], quantity: int = 1):
        """Метод для верификации элементОВ по селектору,
        quantity: это предполагаемое минимальное количество которое он должен найти"""
        try:
            locator = self._is_locator(locator)
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
            locator = self._is_locator(locator)
            return self.wait.until(EC.invisibility_of_element(locator.value))
        except TimeoutException:
            self.logger.error(f'Ошибка, элемент найден и не исчезает {locator.name}={locator.value}')
            raise AssertionError(f'Ошибка, элемент не исчез с экрана {locator.name}={locator.value}')

    def click_element_ac(self, element):
        """Клик с помощью action chains"""
        ActionChains(self.browser).pause(0.1).move_to_element(element).click().perform()

    def move_to_element(self, element):
        self.follow_mouse()
        ActionChains(self.browser).pause(0.1).move_to_element(element)
        return element

    def click_element(self, element):
        """ Клик по элементу

        element: WebElement
        принимает WebElement, клик по WebElement
        """
        for i in range(RETRY, 0, -1):
            try:
                element.click()
                self.logger.info('клик по элементу')
                break
            except (StaleElementReferenceException, ElementClickInterceptedException):
                sleep(i)
                if i == 1:
                    raise AssertionError('Ошибка, не кликнуть по элементу')

    def click_nth_child(self, element, locator, index: int = 0):
        """ В найденном элементе (например таблице) находит элементы с одинаковым css_selector
         и клик по порядковому номеру (index) """
        locator = self._is_locator(locator)
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

    def wait_time(self, time: int = 1):
        sleep(time)
        return self

    def open_url(self, url):
        self.browser.get(url)
        self.wait.until(lambda driver: self.browser.execute_script('return document.readyState') == 'complete')
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

    def _is_locator(self, locator: (str, Enum, tuple[Enum, Enum])) -> Enum:
        """ Приводит локатор к виду Enum """
        if isinstance(locator, Enum):
            return locator
        elif isinstance(locator, tuple):
            selector = (By.CSS_SELECTOR, locator[0].value[1] + ' ' + locator[1].value[1])
            return Enum('NewLocator', [('selector', selector)]).selector
        elif isinstance(locator, str):
            selector = (By.CSS_SELECTOR, locator)
            return Enum('NewLocator', [('selector', selector)]).selector

    def fill_in_fields(self, model_input=None):
        if model_input is not None:
            list_model = dir(model_input)

            list_fields = [attribute for attribute in list_model if attribute.endswith('_attribute')]

            for field in list_fields:
                if model_input.__getattribute__(field) is not None:
                    model_input.__getattribute__(field).set_value()

    def scroll_to(self, element, offset_x=0, offset_y=0):
        x = element.location['x'] + offset_x
        y = element.location['y'] + offset_y
        self.browser.execute_script(f"window.scrollTo({x}, {y})")
        return element

    def follow_mouse(self):
        script = """
        // Create mouse following image.
        var seleniumFollowerImg = document.createElement("img");
        // Set image properties.
        seleniumFollowerImg.setAttribute('src', 'data:image/png;base64,'
            + 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAeCAQAAACGG/bgAAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAA'
            + 'HsYAAB7GAZEt8iwAAAAHdElNRQfgAwgMIwdxU/i7AAABZklEQVQ4y43TsU4UURSH8W+XmYwkS2I0'
            + '9CRKpKGhsvIJjG9giQmliHFZlkUIGnEF7KTiCagpsYHWhoTQaiUUxLixYZb5KAAZZhbunu7O/PKf'
            + 'e+fcA+/pqwb4DuximEqXhT4iI8dMpBWEsWsuGYdpZFttiLSSgTvhZ1W/SvfO1CvYdV1kPghV68a3'
            + '0zzUWZH5pBqEui7dnqlFmLoq0gxC1XfGZdoLal2kea8ahLoqKXNAJQBT2yJzwUTVt0bS6ANqy1ga'
            + 'VCEq/oVTtjji4hQVhhnlYBH4WIJV9vlkXLm+10R8oJb79Jl1j9UdazJRGpkrmNkSF9SOz2T71s7M'
            + 'SIfD2lmmfjGSRz3hK8l4w1P+bah/HJLN0sys2JSMZQB+jKo6KSc8vLlLn5ikzF4268Wg2+pPOWW6'
            + 'ONcpr3PrXy9VfS473M/D7H+TLmrqsXtOGctvxvMv2oVNP+Av0uHbzbxyJaywyUjx8TlnPY2YxqkD'
            + 'dAAAAABJRU5ErkJggg==');
        seleniumFollowerImg.setAttribute('id', 'selenium_mouse_follower');
        seleniumFollowerImg.setAttribute('style', 'position: absolute; z-index: 99999999999; pointer-events: none;');
        // Add mouse follower to the web page.
        document.body.appendChild(seleniumFollowerImg);
        document.onmousemove = function(e) {
            const mousePointer = document.getElementById('selenium_mouse_follower');
            mousePointer.style.left = e.pageX + 'px';
            mousePointer.style.top = e.pageY + 'px';
        }
        """
        self.browser.execute_script(script)
