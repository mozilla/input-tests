#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# The Original Code is Firefox Input
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
#                 Dave Hunt
#                 David Burns
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
Created on Mar 8, 2011
'''

from selenium import selenium
from vars import ConnectionParameters
import unittest

import beta_feedback_page

class TestFeedbackTypeFilter(unittest.TestCase):
    _beta_type_bar_xpath = "//div[@id='filter_type']//li"
    _beta_type_bar_xpath_prefix = "//div[@id='filter_type']//li["
    _beta_type_bar_xpath_suffix = "]//strong"

    _beta_type_svg_locator_prefix = "css=svg * tspan:contains("
    _beta_type_svg_locator_suffix = ")"

    def go_to_search_results_page(self):
        self.selenium.open('/beta/search')

    def get_types_from_beta_type_bar_xpath(self):
        """

        Returns a list of type names from the the Feedback by Type filter bar

        """
        type_count = self.selenium.get_xpath_count(self._beta_type_bar_xpath)
        return ([self.selenium.get_text(self.get_beta_type_bar_xpath(i + 1)) for i in range(type_count)])

    def get_beta_type_bar_xpath(self, nth):
        """

        Returns an xpath for the nth type name in the Feedback by Type filter bar

        """
        return self._beta_type_bar_xpath_prefix + str(nth) + self._beta_type_bar_xpath_suffix

    def get_beta_type_svg_locator(self, type_name):
        """

        Returns a locator for a type legend key in the SVG document

        """
        return self._beta_type_svg_locator_prefix + type_name + self._beta_type_svg_locator_suffix

    def compare_type_bar_text_to_type_svg_text(self):
        """

        Compares the type names from the Feedback by Type filter bar to the
        legend key names in the SVG document

        """
        type_names = self.get_types_from_beta_type_bar_xpath()
        for type_name in type_names:
            locator = self.get_beta_type_svg_locator(type_name)
            if not self.selenium.is_element_present(locator):
                page_title = self.selenium.get_title()
                raise Exception("Expected SVG legend key '" + type_name + "' not found on '" + page_title + "' page.")

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_beta_feedback_can_be_filtered_by_all_expected_feedback_types(self):
        """

        1. Verify that the types in the filter bar match the types in the SVG document legend on the base page
        2. Verify that the types in the filter bar match the types in the SVG document legend on the search page

        """
        beta_feedback_pg = beta_feedback_page.BetaFeedbackPage(self.selenium)

        beta_feedback_pg.go_to_beta_feedback_page()
        self.compare_type_bar_text_to_type_svg_text()
        self.go_to_search_results_page()
        self.compare_type_bar_text_to_type_svg_text()

if __name__ == "__main__":
    unittest.main()
