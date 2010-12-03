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
# Portions created by the Initial Developer are Copyright (C) 2___
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
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

Created on Nov 30, 2010

'''

from datetime import date, timedelta
from selenium import selenium
import vars
import unittest

import feedback_page
import search_results_page


class SearchDates(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(vars.ConnectionParameters.server, vars.ConnectionParameters.port, vars.ConnectionParameters.browser, vars.ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(vars.ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_preset_date_filters(self):
        """

        This testcase covers # 13605 & 13606 in Litmus
        1. Verifies the preset date filters of 1, 7, and 30 days

        """
        sel = self.selenium
        feedback_obj = feedback_page.FeedbackPage(sel)
        search_page_obj = search_results_page.SearchResultsPage(sel)

        feedback_obj.go_to_feedback_page()
        # Assert disabled for Bug 616299
        # self.assertEqual(search_page_obj.get_current_days(), "30d")

        day_filters = ((1, "1d", "Last day"), (7, "7d", "Last 7 days"), (30, "30d", "Last 30 days"))
        for days in day_filters:
            self.assertEqual(search_page_obj.get_days_tooltip(days[1]), days[2])
            search_page_obj.click_days(days[1])
            self.assertEqual(search_page_obj.get_current_days(), days[1])
            search_page_obj.verify_preset_days_search_page_url(days[0])
            # TODO: Check results are within the expected date range, possibly by navigating to the last page and checking the final result is within range. Currently blocked by bug 615844.

    def test_custom_date_filter(self):
        """

        This testcase covers # 13605, 13606 & 13715 in Litmus
        1. Verifies the calendar is displayed when filtering on custom dates
        2. Verifies date-start=<date> and end-date=<date> in the url

        """
        sel = self.selenium
        feedback_obj = feedback_page.FeedbackPage(sel)
        search_page_obj = search_results_page.SearchResultsPage(sel)

        feedback_obj.go_to_feedback_page()
        self.assertEqual(search_page_obj.get_custom_dates_tooltip(), "Custom")

        start_date = date.today() - timedelta(days=3)
        end_date = date.today() - timedelta(days=1)

        search_page_obj.filter_by_custom_dates(start_date, end_date)
        search_page_obj.verify_custom_dates_search_page_url(start_date, end_date)
        # TODO: Check results are within the expected date range, possibly by navigating to the first/last pages and checking the final result is within range. Currently blocked by bug 615844.

        # Check that the relevant days preset link is highlighted when the applied custom date filter matches it
        day_filters = ((1, "1d"), (7, "7d"), (30, "30d"))
        for days in day_filters:
            start_date = date.today() - timedelta(days=days[0])
            search_page_obj.filter_by_custom_dates(start_date, date.today())
            self.assertFalse(search_page_obj.is_custom_date_filter_visible())
            search_page_obj.verify_custom_dates_search_page_url(start_date, date.today())
            self.assertEqual(search_page_obj.get_current_days(), days[1])

if __name__ == "__main__":
    unittest.main()
