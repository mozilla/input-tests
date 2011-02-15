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

class TestExpandAndFilterLocaleList(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_expand_and_filter_locale_list(self):
        """

        This testcase covers # 15087 in Litmus

        """
        beta_feedback_pg = beta_feedback_page.BetaFeedbackPage(self.selenium)
        search_results_pg = search_results_page.SearchResultsPage(self.selenium)

        beta_feedback_pg.go_to_beta_feedback_page()

        self.assertEqual(int(beta_feedback_pg.locale_count), 10)
        beta_feedback_pg.click_more_locales_link()
        self.assertTrue(beta_feedback_pg.is_extra_locales_list_visible)
        beta_feedback_pg.click_locale("china")

        self.assertTrue(0 < beta_feedback_pg.message_count)
        self.assertEqual(beta_feedback_pg.first_message_locale, "Chinese (Simplified)")
        self.assertEqual(search_results_pg.locale_from_url, 'zh-CN')

if __name__ == "__main__":
    unittest.main()
