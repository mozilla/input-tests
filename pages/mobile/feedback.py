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
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
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

from pages.base import InputBasePage


class FeedbackPage(InputBasePage):

    _page_title = 'Welcome :: Firefox Input'

    #header
    _search_locator = 'id=id_q'

    _feed_tab_locator = 'id=tab-feed'
    _statistics_tab_locator = 'id=tab-stats'
    _settings_tab_locator = 'id=tab-settings'

    #body
    _feed_page_locator = 'id=feed'
    _statistics_page_locator = 'id=stats'
    _trends_page_locator = 'id=trends'
    _settings_page_locator = 'id=settings'

    def go_to_feedback_page(self):
        self.selenium.open('/')
        self.is_the_current_page

    def search_for(self, search_string):
        self.selenium.type(self._search_locator, search_string)
        self.selenium.key_press(self._search_locator, '\\13')
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_feed_tab(self):
        self.selenium.click(self._feed_tab_locator)
        self.wait_for_element_visible(self._feed_page_locator)

    def click_statistics_tab(self):
        self.selenium.click(self._statistics_tab_locator)
        self.wait_for_element_visible(self._statistics_page_locator)

    def click_settings_tab(self):
        self.selenium.click(self._settings_tab_locator)
        self.wait_for_element_visible(self._settings_page_locator)

    @property
    def is_feed_visible(self):
        return self.selenium.is_visible(self._feed_page_locator)

    @property
    def is_statistics_visible(self):
        return self.selenium.is_visible(self._statistics_page_locator)

    @property
    def is_settings_visible(self):
        return self.selenium.is_visible(self._settings_page_locator)
