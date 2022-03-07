from enum import Enum
from selenium.webdriver.common.by import By
from cssselect import GenericTranslator, SelectorError


class Locator:

    @staticmethod
    def is_locator(locator: (str, Enum, tuple[Enum, Enum])) -> Enum:
        """
        Приводит локатор к виду Enum
        """
        if isinstance(locator, Enum):
            return locator
        elif isinstance(locator, tuple):
            selector = (By.CSS_SELECTOR, locator[0].value[1] + ' ' + locator[1].value[1])
            return Enum('NewLocator', [('selector', selector)]).selector
        elif isinstance(locator, str):
            selector = (By.CSS_SELECTOR, locator)
            return Enum('NewLocator', [('selector', selector)]).selector

    @staticmethod
    def to_xpath(locator, text):
        """
        Конвертирует CSS селектор в XPath.
        Если передать валидный XPath, то вернёт его без изменений.
        """

        condition = f"[contains(., {GenericTranslator().xpath_literal(text)})]"

        return f"{GenericTranslator().css_to_xpath(locator)}{condition}"

