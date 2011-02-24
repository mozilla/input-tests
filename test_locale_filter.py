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
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Tobias Markus <tobbi.bugs@googlemail.com>
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


from selenium import selenium
from vars import ConnectionParameters
import unittest

import beta_feedback_page
import search_results_page

class TestLocaleFilter(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_locale_filter(self):
        """

        This testcase covers # 15087 in Litmus
        1. Verify the initial locale count is 10
        2. Verify that clicking a specific locale in the top 10 list of locales only shows input specific for that locale
        """
        beta_feedback_pg = beta_feedback_page.BetaFeedbackPage(self.selenium)
        search_results_pg = search_results_page.SearchResultsPage(self.selenium)

        beta_feedback_pg.go_to_beta_feedback_page()
        beta_feedback_pg.select_product('firefox')
        beta_feedback_pg.select_version(2, by='index')

        self.assertEqual(beta_feedback_pg.locale_count, 10)
        num_messages = beta_feedback_pg.locale_message_count("de", by="code")
        beta_feedback_pg.click_locale("germany")

        self.assertTrue(beta_feedback_pg.message_count <= num_messages)
        self.assertEqual(beta_feedback_pg.first_message_locale, "German (Germany)")
        self.assertEqual(search_results_pg.locale_from_url, "de")

    def test_extra_locale_filter(self):
        """

        This testcase covers # 15087 in Litmus
        1. Verify the initial locale count is 10
        2. Verify clicking the More locales link shows additional locales
        3. Verify that clicking a specific locale in the extended list of locales only shows input specific for that locale
        """
        beta_feedback_pg = beta_feedback_page.BetaFeedbackPage(self.selenium)
        search_results_pg = search_results_page.SearchResultsPage(self.selenium)

        beta_feedback_pg.go_to_beta_feedback_page()
        beta_feedback_pg.select_product('firefox')
        beta_feedback_pg.select_version(2, by='index')

        self.assertEqual(beta_feedback_pg.locale_count, 10)
        beta_feedback_pg.click_more_locales_link()
        loc_name = beta_feedback_pg.locale_name_by_index(11)
        loc_code = beta_feedback_pg.locale_code_by_index(11)
        num_messages = beta_feedback_pg.locale_message_count(11)
        beta_feedback_pg.click_locale(11, by="index")

        self.assertTrue(beta_feedback_pg.message_count <= num_messages)
        self.assertEqual(beta_feedback_pg.first_message_locale, loc_name)
        self.assertEqual(search_results_pg.locale_from_url, loc_code)

if __name__ == "__main__":
    unittest.main()
