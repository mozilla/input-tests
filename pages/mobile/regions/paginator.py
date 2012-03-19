#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class Paginator(BasePage):

    _older_feedback_button_locator = (By.CSS_SELECTOR, 'div.pager a.next')
    _newer_feedback_button_locator = (By.CSS_SELECTOR, 'div.pager .prev')

    def click_older_feedback_button(self):
        self.selenium.find_element(*self._older_feedback_button_locator).click()

    def click_newer_feedback_button(self):
        self.selenium.find_element(*self._newer_feedback_button_locator).click()

    @property
    def is_older_feedback_button_disabled(self):
        is_disabled = self.selenium.find_element(*self._older_feedback_button_locator).get_attribute('class')
        return "disabled" in is_disabled

    @property
    def is_newer_feedback_button_disabled(self):
        is_disabled = self.selenium.find_element(*self._newer_feedback_button_locator).get_attribute('class')
        return "disabled" in is_disabled
