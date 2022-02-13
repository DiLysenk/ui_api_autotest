from pageobject.komtek_net.kom_tek import KomTekPageObject


class TestKomTek:

    def test_search_goods(self, browser):
        main_page = KomTekPageObject(browser, search_goods='IdeaTab K10 TB-X6C6F 64Gb')
        main_page.open_url(main_page.url)
        main_page.fill_in_fields(main_page)
        main_page.wait_time(5)
        assert main_page.find_by_text('ZA8N0012RU', locator='[itemprop="name"]')

