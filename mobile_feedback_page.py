import input_base_page


class FeedbackPage(input_base_page.InputBasePage,):

    _page_title = 'Welcome :: Firefox Input'

    #header
    _search_locator = 'id=id_q'

    _feed_header_locator = 'id=tab-feed'
    _statistics_header_locator = 'id=tab-stats'
    _settings_header_locator = 'id=tab-settings'

    #body
    _feed_body_locator = 'id=feed'
    _statistics_body_locator = 'id=stats'
    _trends_body_locator = 'id=trends'
    _settings_body_locator = 'id=settings'

    def go_to_feedback_page(self):
        self.selenium.open('/')
        self.is_the_current_page

    def search_for(self, search_string):
        self.selenium.type(self._search_locator, search_string)
        self.selenium.key_press(self._search_locator, '\\13')
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_feed(self):
        self.selenium.click(self._feed_header_locator)
        self.wait_for_element_visible(self._feed_body_locator)

    def click_statistics(self):
        self.selenium.click(self._statistics_header_locator)
        self.wait_for_element_visible(self._statistics_body_locator)

    def click_settings(self):
        self.selenium.click(self._settings_header_locator)
        self.wait_for_element_visible(self._settings_body_locator)

    @property
    def visible_page(self):
        if self.selenium.is_visible(self._feed_body_locator):
            return "feed"

        if self.selenium.is_visible(self._statistics_body_locator):
            return "statistics"

        if self.selenium.is_visible(self._trends_body_locator):
            return "trends"

        if self.selenium.is_visible(self._settings_body_locator):
            return "settings"
