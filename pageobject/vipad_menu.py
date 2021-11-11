from base_page import BasePage


class VipadMenu(BasePage):

    def click_menu(self, locator):
        self.click_locator(locator)

    def grab_varians(self, locator):
        self.is_visible(locator)
        options = self.are_visible('options')
        text_options = [i.text for i in options]
        return text_options


    def click_in_option(self, locator, text_option):
        self.grab_varians(locator)

