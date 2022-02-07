from pageobject.citilink.citylink_page import CityPO
import pytest


@pytest.mark.usefixtures('log_fixture')
class TestCytiLink:

    def test_poisk(self, browser):
        city_main_page = CityPO(browser, poisk='NVIDIA GeForce RTX 3060')
        city_main_page.open_url(city_main_page.url)
        city_main_page.fill_in_the_fields(city_main_page)


    # def sorted(self, browser):
    #     city_main_page = CityPO(browser, sorted_platform='AMD')
    #     city_main_page.open_url(city_main_page.url)
    #     city_main_page.open(CityCSS.my_configuration)



