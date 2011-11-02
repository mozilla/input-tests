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
#   Teodosia Pop <teodosia.pop@softvision.ro>
#   Matt Brandt <mbrandt@mozilla.com>
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


class Message(Page):

    _type_locator = (By.CSS_SELECTOR, '.type')
    _body_locator = (By.CSS_SELECTOR, '.body')
    _time_locator = (By.CSS_SELECTOR, 'time')
    _platform_locator = (By.CSS_SELECTOR, '.meta li:nth-child(2) a')
    _locale_locator = (By.CSS_SELECTOR, '.meta li:nth-child(3) a')
    _site_locator = (By.CSS_SELECTOR, '.meta li:nth-child(4)')
    _more_options_locator = (By.CSS_SELECTOR, '.options')
    _copy_user_agent_locator = (By.CSS_SELECTOR, '.options .copy_ua')
    _copy_user_agent_locator = (By.CSS_SELECTOR, '.options .copy_ua')
    _translate_message_locator = (By.CSS_SELECTOR, 'li:nth(1) a')
    _tweet_this_locator = (By.CSS_SELECTOR, '.options .twitter')

    def __init__(self, testsetup, element):
        Page.__init__(self, testsetup)
        self._root_element = element

    def click_platform(self):
        self._root_element.find_element(*self._platform_locator).click()

    def click_locale(self):
        self._root_element.find_element(*self._locale_locator).click()

    def click_timestamp(self):
        self._root_element.find_element(*self._time_locator).click()

    @property
    def is_platform_visible(self):
        return self.is_element_visible(self._platform_locator)

    @property
    def is_locale_visible(self):
        return self.is_element_visible(self._locale_locator)

    @property
    def type(self):
        return self._root_element.find_element(*self._type_locator).text

    @property
    def body(self):
        return self._root_element.find_element(*self._body_locator).text

    @property
    def time(self):
        return self._root_element.find_element(*self._time_locator).text

    @property
    def platform(self):
        return self._root_element.find_element(*self._platform_locator).text

    @property
    def locale(self):
        return self._root_element.find_element(*self._locale_locator).text

    @property
    def site(self):
        return self._root_element.find_element(*self._site_locator).text
