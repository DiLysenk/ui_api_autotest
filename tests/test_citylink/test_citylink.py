from pageobject.citilink.citylink_page import CityPO
import pytest


@pytest.mark.usefixtures('log_fixture')
class TestCytiLink:

    def test_poisk(self, browser):
        cp = CityPO(browser, poisk='NVIDIA GeForce RTX 3060')
        cp.navigate_to(cp.url)
        cp.fill_in_the_fields(cp)

