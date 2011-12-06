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
#   Vishal
#   Dave Hunt <dhunt@mozilla.com>
#   Bebe <florin.strugariu@softvision.ro>
#   Teodosia Pop <teodosia.pop@softvision.ro>
#   Alex Lakatos <alex.lakatos@softvision.ro>
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
from selenium.webdriver.common.keys import Keys

from pages.base import BasePage
from pages.desktop.regions.message import Message


class FeedbackPage(BasePage):

    _page_title = 'Welcome :: Firefox Input'

    _warning_heading_locator = (By.CSS_SELECTOR, '#message-warning h3')
    _search_box = (By.ID, 'id_q')
    _chart_locator = (By.ID, 'feedback-chart')
    _total_message_count_locator = (By.CSS_SELECTOR, '#big-count p')
    _total_message_count_heading_locator = (By.CSS_SELECTOR, '#big-count h3')
    _messages_column_heading_locator = (By.CSS_SELECTOR, '#messages h2')
    _messages_locator = (By.CSS_SELECTOR, '#messages.block ul li.message')

    def go_to_feedback_page(self):
        self.selenium.get(self.base_url + '/')
        self.is_the_current_page

    def click_search_box(self):
        self.selenium.find_element(*self._search_box).click()

    @property
    def locale_filter(self):
        from pages.desktop.regions.locale_filter import LocaleFilter
        return LocaleFilter(self.testsetup)

    @property
    def platform_filter(self):
        from pages.desktop.regions.platform_filter import PlatformFilter
        return PlatformFilter.CheckboxFilter(self.testsetup)

    @property
    def type_filter(self):
        from pages.desktop.regions.type_filter import TypeFilter
        return TypeFilter.CheckboxFilter(self.testsetup)

    @property
    def common_words_filter(self):
        from pages.desktop.regions.common_words import CommonWordsRegion
        return CommonWordsRegion(self.testsetup)

    @property
    def sites_filter(self):
        from pages.desktop.regions.sites_filter import SitesFilter
        return SitesFilter(self.testsetup)

    @property
    def product_filter(self):
        from pages.desktop.regions.product_filter import ProductFilter
        return ProductFilter.ComboFilter(self.testsetup)

    @property
    def date_filter(self):
        from pages.desktop.regions.date_filter import DateFilter
        return DateFilter(self.testsetup)

    def search_for(self, search_string):
        search_box = self.selenium.find_element(*self._search_box)
        search_box.send_keys(search_string)
        search_box.send_keys(Keys.RETURN)

    @property
    def search_box(self):
        return self.selenium.find_element(*self._search_box).get_attribute('value')

    @property
    def search_box_placeholder(self):
        return self.selenium.find_element(*self._search_box).get_attribute('placeholder')

    @property
    def message_column_heading(self):
        return self.selenium.find_element(*self._messages_column_heading_locator).text

    @property
    def total_message_count(self):
        return self.selenium.find_element(*self._total_message_count_locator).text

    @property
    def total_message_count_heading(self):
        """Get the total messages header value."""
        return self.selenium.find_element(*self._total_message_count_heading_locator).text

    @property
    def messages(self):
        return [Message(self.testsetup, message) for message in self.selenium.find_elements(*self._messages_locator)]

    @property
    def is_chart_visible(self):
        return self.is_element_visible(self._chart_locator)

    @property
    def warning_heading(self):
        return self.selenium.find_element(*self._warning_heading_locator).text
