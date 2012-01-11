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
#   Bebe <florin.strugariu@softvision.ro>
#   Dave Hunt <dhunt@mozilla.com>
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
