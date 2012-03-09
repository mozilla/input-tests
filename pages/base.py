#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib
from urlparse import urlparse

from selenium.webdriver.common.by import By

from page import Page


class BasePage(Page):

    _older_messages_link_locator = (By.CSS_SELECTOR, '.pager .older')
    _newer_messages_link_locator = (By.CSS_SELECTOR, '.pager .newer')

    @property
    def header(self):
        from pages.desktop.regions.header import Header
        return Header(self.testsetup)

    @property
    def footer(self):
        from pages.desktop.regions.footer import Footer
        return Footer(self.testsetup)

    def click_older_messages(self):
        """Navigates to the previous page of older messages."""
        self.selenium.find_element(*self._older_messages_link_locator).click()

    def click_newer_messages(self):
        """Navigates to the next page of newer messages."""
        self.selenium.find_element(*self._newer_messages_link_locator).click()

    @property
    def older_messages_link(self):
        return self.selenium.find_element(*self._older_messages_link_locator).text

    @property
    def newer_messages_link(self):
        return self.selenium.find_element(*self._newer_messages_link_locator).text

    @property
    def is_older_messages_link_visible(self):
        return self.is_element_visible(self._older_messages_link_locator)

    @property
    def is_newer_messages_link_visible(self):
        return self.is_element_visible(self._newer_messages_link_locator)

    @property
    def is_older_messages_link_enabled(self):
        return not 'inactive' in self.selenium.find_element(*self._older_messages_link_locator).get_attribute('class')

    @property
    def is_newer_messages_link_enabled(self):
        return not 'inactive' in self.selenium.find_element(*self._newer_messages_link_locator).get_attribute('class')

    def _value_from_url(self, param):
        """Returns the value for the specified parameter in the URL."""
        url = urlparse(self.selenium.current_url)
        if param in url[4]:
            params = dict([part.split('=') for part in url[4].split('&')])
            return urllib.unquote(params[param])

    @property
    def feedback_type_from_url(self):
        """Returns the feedback type (praise, issues, ideas) from the current location URL."""
        return self._value_from_url("s")

    @property
    def platform_from_url(self):
        """Returns the platform from the current location URL."""
        return self._value_from_url("platform")

    @property
    def product_from_url(self):
        """Returns the product from the current location URL.

        NOTE: if the site is on the homepage (not on the search page) and default/latest
        version is selected then the URL will not contain the product parameter.

        """
        return self._value_from_url("product")

    @property
    def search_term_from_url(self):
        """Returns the search value from the current location URL."""
        return self._value_from_url("q")

    @property
    def version_from_url(self):
        """Returns the version from the current location URL.

        NOTE: if the site is on the homepage (not on the search page) and default/latest
        version is selected then the URL will not contain the version parameter.

        """
        return self._value_from_url("version")

    @property
    def date_start_from_url(self):
        """Returns the date_start value from the current location URL."""
        return self._value_from_url("date_start")

    @property
    def date_end_from_url(self):
        """Returns the date_end value from the current location URL."""
        return self._value_from_url("date_end")

    @property
    def page_from_url(self):
        """Returns the page value from the current location URL."""
        return int(self._value_from_url("page"))

    @property
    def locale_from_url(self):
        """Returns the locale value from the current location URL."""
        return self._value_from_url("locale")
