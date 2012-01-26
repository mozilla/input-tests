#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base import BasePage
from pages.desktop.regions.message import Message


class FeedbackPage(BasePage):

    _page_title = 'Welcome :: Firefox Input'

    _warning_heading_locator = (By.CSS_SELECTOR, '#message-warning h3')
    _search_box = (By.ID, 'id_q')
    _chart_locator = (By.ID, 'feedback-chart')
    _total_message_count_locator = (By.CSS_SELECTOR, '#big-count p')
    _total_message_count_heading_locator = (By.CSS_SELECTOR, '#big-count h3')
    _messages_column_heading_locator = (By.CSS_SELECTOR, '#messages h2')
    _messages_locator = (By.CSS_SELECTOR, '#messages.block ul li.message')

    def go_to_feedback_page(self):
        self.selenium.get(self.base_url + '/')
        self.is_the_current_page

    def click_search_box(self):
        self.selenium.find_element(*self._search_box).click()

    @property
    def locale_filter(self):
        from pages.desktop.regions.locale_filter import LocaleFilter
        return LocaleFilter(self.testsetup)

    @property
    def platform_filter(self):
        from pages.desktop.regions.platform_filter import PlatformFilter
        return PlatformFilter.CheckboxFilter(self.testsetup)

    @property
    def type_filter(self):
        from pages.desktop.regions.type_filter import TypeFilter
        return TypeFilter.CheckboxFilter(self.testsetup)

    @property
    def common_words_filter(self):
        from pages.desktop.regions.common_words import CommonWordsRegion
        return CommonWordsRegion(self.testsetup)

    @property
    def sites_filter(self):
        from pages.desktop.regions.sites_filter import SitesFilter
        return SitesFilter(self.testsetup)

    @property
    def product_filter(self):
        from pages.desktop.regions.product_filter import ProductFilter
        return ProductFilter.ComboFilter(self.testsetup)

    @property
    def date_filter(self):
        from pages.desktop.regions.date_filter import DateFilter
        return DateFilter(self.testsetup)

    def search_for(self, search_string):
        search_box = self.selenium.find_element(*self._search_box)
        search_box.send_keys(search_string)
        search_box.send_keys(Keys.RETURN)

    @property
    def search_box(self):
        return self.selenium.find_element(*self._search_box).get_attribute('value')

    @property
    def search_box_placeholder(self):
        return self.selenium.find_element(*self._search_box).get_attribute('placeholder')

    @property
    def message_column_heading(self):
        return self.selenium.find_element(*self._messages_column_heading_locator).text

    @property
    def total_message_count(self):
        return self.selenium.find_element(*self._total_message_count_locator).text

    @property
    def total_message_count_heading(self):
        """Get the total messages header value."""
        return self.selenium.find_element(*self._total_message_count_heading_locator).text

    @property
    def messages(self):
        return [Message(self.testsetup, message) for message in self.selenium.find_elements(*self._messages_locator)]

    @property
    def is_chart_visible(self):
        return self.is_element_visible(self._chart_locator)

    @property
    def warning_heading(self):
        return self.selenium.find_element(*self._warning_heading_locator).text
