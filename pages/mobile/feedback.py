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
    def paginator(self):
        from pages.mobile.regions.paginator import Paginator
        return Paginator(self.testsetup)
