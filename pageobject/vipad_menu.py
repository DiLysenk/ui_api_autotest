from base_page import BasePage


class VipadMenu(BasePage):

    def click_menu(self, locator):
        self.click(locator)

    def grab_variants(self, locator):
        self.find_visible(locator)
        options = self.are_visible('options')
        text_options = [i.text for i in options]
        return text_options

