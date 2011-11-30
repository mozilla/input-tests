#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla.
#
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Dave Hunt <dhunt@mozilla.com>
#   Bebe <florin.strugariu@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from selenium.webdriver.common.by import By

from page import Page


class LocaleFilter(Page):

    _locales_locator = (By.XPATH, "id('filter_locale')//li[..[not(@class='extra')]][input[@name='locale']]")
    _more_locales_link_locator = (By.CSS_SELECTOR, '#filter_locale .more')
    _more_locales_locator = (By.CSS_SELECTOR, '#filter_locale .extra li')
    _total_message_count_locator = (By.CSS_SELECTOR, '#filter_locale .bars')

    @property
    def total_message_count(self):
        return self.selenium.find_element(*self._total_message_count_locator).get_attribute('data-total')

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
        _name_locator = (By.CSS_SELECTOR, 'label > strong')
        _message_count_locator = (By.CLASS_NAME, 'count')
        _message_percentage_locator = (By.CLASS_NAME, 'perc')

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
            return self.selenium.execute_script('return arguments[0].textContent', message_count)

        @property
        def message_percentage(self):
            return self._root_element.find_element(*self._message_percentage_locator).text

        def select(self):
            self._root_element.find_element(*self._checkbox_locator).click()

        def percentage(self, total_messages):
            return round((float(self.message_count) / float(total_messages)) * 100)
