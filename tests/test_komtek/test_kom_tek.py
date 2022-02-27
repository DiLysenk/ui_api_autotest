from pageobject.komtek_net.kom_tek import KomTekPageObject


class TestKomTek:

    def test_search_goods(self, browser):
        main_page = KomTekPageObject(browser, search_goods='IdeaTab K10 TB-X6C6F 64Gb')
        main_page.open_url(main_page.url)
        main_page.fill_in_fields(main_page)
        assert main_page.find_by_text('ZA8N0012RU', locator='[itemprop="name"]')

    def test_pagination(self, browser):
        main_page = KomTekPageObject(browser, pagination='50')
        main_page.navigate_to_note_book_table()
        main_page.fill_in_fields(main_page)
        assert len(main_page.are_visible('li.item', quantity=50)) == 50
