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
# The Original Code is Firefox Input.
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
#                 Dave Hunt <dhunt@mozilla.com>
#                 Bebe <florin.strugariu@softvision.ro>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex.lakatos@softvision.ro>
#                 Matt Brandt <mbrandt@mozilla.com>
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
'''
Created on Nov 19, 2010
'''
import input_base_page
import product_filter_region
import date_filter_region
import locale_filter_region
import platform_filter_region
import message_region
import type_filter_region
import common_words_region
import sites_filter_region
import header_region
import footer_region


class FeedbackPage(input_base_page.InputBasePage):

    _page_title = 'Welcome :: Firefox Input'

    _warning_heading_locator = "css=#message-warning h3"
    _type_issues_locator = "css=#filters a:contains(Issues)"
    _search_box = "id_q"
    _chart_locator = "id=feedback-chart"
    _total_message_count_locator = "css=#big-count p"
    _total_message_count_heading_locator = "css=#big-count h3"
    _messages_column_heading_locator = "css=#messages h2"
    _messages_locator = "css=div#messages.block ul li.message"

    def go_to_feedback_page(self):
        self.selenium.open('/')
        self.is_the_current_page

    def click_search_box(self):
        self.selenium.click(self._search_box)

    @property
    def locale_filter(self):
        return locale_filter_region.LocaleFilter(self.testsetup)

    @property
    def platform_filter(self):
        return platform_filter_region.PlatformFilter.CheckboxFilter(self.testsetup)

    @property
    def type_filter(self):
        return type_filter_region.TypeFilter.CheckboxFilter(self.testsetup)

    @property
    def common_words_filter(self):
        return common_words_region.CommonWordsRegion(self.testsetup)

    @property
    def sites_filter_region(self):
        return sites_filter_region.SitesFilterRegion(self.testsetup)

    @property
    def product_filter(self):
        return product_filter_region.ProductFilter.ComboFilter(self.testsetup)

    @property
    def date_filter(self):
        return date_filter_region.DateFilter(self.testsetup)

    @property
    def header_region(self):
        return header_region.Header(self.testsetup)

    @property
    def footer_region(self):
        return footer_region.Footer(self.testsetup)

    def search_for(self, search_string):
        self.selenium.type(self._search_box, search_string)
        self.selenium.key_press(self._search_box, '\\13')
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def search_box(self):
        return self.selenium.get_value(self._search_box)

    @property
    def search_box_placeholder(self):
        return self.selenium.get_attribute(self._search_box + "@placeholder")

    @property
    def message_column_heading(self):
        return self.selenium.get_text(self._messages_column_heading_locator)

    @property
    def total_message_count(self):
        return self.selenium.get_text(self._total_message_count_locator)

    @property
    def total_message_count_heading(self):
        """
        Get the total messages header value
        """
        return self.selenium.get_text(self._total_message_count_heading_locator)

    @property
    def message_count(self):
        return int(self.selenium.get_css_count(self._messages_locator))

    @property
    def messages(self):
        return [message_region.Message(self.testsetup, i + 1) for i in range(self.message_count)]

    def message(self, index):
        return message_region.Message(self.testsetup, index)

    @property
    def search_box_placeholder(self):
        return self.selenium.get_attribute(self._search_box + "@placeholder")

    @property
    def is_chart_visible(self):
        return self.is_element_visible(self._chart_locator)

    @property
    def warning_heading(self):
        return self.selenium.get_text(self._warning_heading_locator)
