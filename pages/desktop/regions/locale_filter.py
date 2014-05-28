#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import Page


class LocaleFilter(Page):

    _locales_locator = (By.CSS_SELECTOR, "ul[name='locale'] li")
    _more_locales_link_locator = (By.CSS_SELECTOR, '#filter_locale .more')
    _more_locales_locator = (By.CSS_SELECTOR, '#filter_locale .extra li')
    _total_message_count_locator = (By.CSS_SELECTOR, '#filter_locale .bars')

    @property
    def total_message_count(self):
        return int(self.selenium.find_element(*self._total_message_count_locator).get_attribute('data-total'))

    @property
    def are_more_locales_visible(self):
        return self.is_element_visible(self._more_locales_locator)

    def show_more_locales(self):
        self.selenium.find_element(*self._more_locales_link_locator).click()

    def locale(self, value):
        for locale in self.locales:
            if locale.name == value:
                return locale
        raise Exception("Locale not found: '%s'. Locales: %s" % (value, [locale.name for locale in self.locales]))

    @property
    def locales(self):
        locales = [self.Locale(self.testsetup, element) for element in self.selenium.find_elements(*self._locales_locator)]
        if self.are_more_locales_visible:
            locales.extend([self.Locale(self.testsetup, element) for element in self.selenium.find_elements(*self._more_locales_locator)])
        return locales

    class Locale(Page):

        _checkbox_locator = (By.TAG_NAME, 'input')
        _name_locator = (By.CSS_SELECTOR, 'label > span:nth-child(2)')
        _message_count_locator = (By.CLASS_NAME, 'count')
        _message_percentage_locator = (By.CLASS_NAME, 'percent')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def is_selected(self):
            return self._root_element.find_element(*self._checkbox_locator).is_selected()

        @property
        def name(self):
            return self._root_element.find_element(*self._name_locator).text

        @property
        def code(self):
            return self._root_element.find_element(*self._checkbox_locator).get_attribute('value')

        @property
        def message_count(self):
            # TODO Use native mouse interactions to hover over element to get the text
            message_count = self._root_element.find_element(*self._message_count_locator)
            return int(self.selenium.execute_script('return arguments[0].textContent', message_count))

        @property
        def message_percentage(self):
            return int(self._root_element.find_element(*self._message_percentage_locator).text.split("%")[0])

        def select(self):
            self._root_element.find_element(*self._checkbox_locator).click()

        def percentage(self, total_messages):
            return round((float(self.message_count) / float(total_messages)) * 100)
