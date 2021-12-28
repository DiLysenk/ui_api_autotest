import pytest
import allure
from pageobject.transport.transport_page import TransportPage


class TestTransport:



    def test_find_bus(self, browser):
        p = TransportPage(browser)
        p.navigate_to(p.URL)
        p.select_transport('Автобус')
        p.fill_number_field('К-271')
        p.press_btn_find()
        assert p.find_by_text('К-271'), 'ожидалось наличие автобуса 198 на странице'


    def test_find_station(self, browser):
        p = TransportPage(browser)
        p.navigate_to(p.URL)
        p.select_transport('Автобус')
        p.fill_name_station('Парнас')
        p.press_btn_find()
        assert p.find_by_text('Парнас'), f'ожидалось наличие Парнас на странице'


    def test_find_street(self, browser):
        p = TransportPage(browser)
        p.navigate_to(p.URL)
        p.select_transport('Автобус')
        p.fill_name_station('Суздальский')
        p.press_btn_find()
        assert p.find_by_text('Суздальский'), f'ожидалось наличие автобуса 198 на странице'