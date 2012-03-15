#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.base import BasePage


class FeedbackPage(BasePage):

    _page_title = 'Welcome :: Firefox Input'

    _feed_tab_locator = (By.ID, 'tab-feed')
    _statistics_tab_locator = (By.ID, 'tab-stats')
    _settings_tab_locator = (By.ID, 'tab-settings')

    _feed_page_locator = (By.ID, 'feed')
    _statistics_page_locator = (By.ID, 'stats')
    _trends_page_locator = (By.ID, 'trends')
    _settings_page_locator = (By.ID, 'settings')

    _search_box = (By.ID, 'id_q')

    _messages_locator = (By.CSS_SELECTOR, 'div.block > ul.messages > li.list-item')

    def go_to_feedback_page(self):
        print 'opening: ' + self.base_url + '/'
        self.selenium.get(self.base_url + '/')
        self.is_the_current_page

    def click_feed_tab(self):
        self.selenium.find_element(*self._feed_tab_locator).click()

    def click_statistics_tab(self):
        self.selenium.find_element(*self._statistics_tab_locator).click()

    def click_settings_tab(self):
        self.selenium.find_element(*self._settings_tab_locator).click()

    def search_for(self, search_string):
        search_box = self.selenium.find_element(*self._search_box)
        search_box.send_keys(search_string)
        search_box.submit()

    @property
    def is_feed_visible(self):
        return self.is_element_visible(self._feed_page_locator)

    @property
    def is_statistics_visible(self):
        return self.is_element_visible(self._statistics_page_locator)

    @property
    def is_settings_visible(self):
        return self.is_element_visible(self._settings_page_locator)

    @property
    def search_box_placeholder(self):
        return self.selenium.find_element(*self._search_box).get_attribute('placeholder')

    @property
    def messages(self):
        from pages.mobile.regions.message import Message
        return [Message(self.testsetup, message) for message in self.selenium.find_elements(*self._messages_locator)]
