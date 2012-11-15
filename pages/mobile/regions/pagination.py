#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class PaginationRegion(BasePage):

    _older_button_locator = (By.CSS_SELECTOR, 'div.pager a.next')
    _newer_button_locator = (By.CSS_SELECTOR, 'div.pager .prev')
    _pager_locator = (By.CSS_SELECTOR, 'div.pager')

    def click_older_button(self):
        self.click_pager()
        self.selenium.find_element(*self._older_button_locator).click()

    def click_newer_button(self):
        self.click_pager()
        self.selenium.find_element(*self._newer_button_locator).click()

    @property
    def is_older_button_disabled(self):
        return "disabled" in self.selenium.find_element(*self._older_button_locator).get_attribute('class')

    @property
    def is_newer_button_disabled(self):
        return "disabled" in self.selenium.find_element(*self._newer_button_locator).get_attribute('class')

    def click_pager(self):
        """We click the footer because of a android scroll issue #3171."""
        self.selenium.find_element(*self._pager_locator).click()
