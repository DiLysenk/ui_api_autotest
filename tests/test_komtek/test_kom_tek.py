from pageobject.komtek_net.kom_tek import KomTekPageObject, KomTekModel


class TestKomTek:

    def test_search_goods(self, browser):
        main_page = KomTekPageObject(browser)
        model = KomTekModel(search_goods='IdeaTab K10 TB-X6C6F 64Gb')
        main_page.open_url(main_page.url)
        main_page.fill_in_fields2(model)
        main_page.wait_time(5)
        assert main_page.find_by_text('ZA8N0012RU', locator='[itemprop="name"]')

    def test_pagination(self, browser):
        main_page = KomTekPageObject(browser, )
        model = KomTekModel(pagination='50')
        main_page.navigate_to_note_book_table()
        main_page.fill_in_fields2(model)
        main_page.wait_time(5)
        assert len(main_page.are_visible('li.item')) == 50
