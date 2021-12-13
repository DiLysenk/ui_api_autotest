import pytest
import allure
from pageobject.transport.transport_page import TransportPage


class TestTransport:



    def test_find_bus(self, browser):
        p = TransportPage(browser)
        p.navigate_to(p.URL)
        p.select_transport('Автобус')
        p.fill_number_field('198')
        p.fill_name_station('Парнас')
        p.press_btn_find()



