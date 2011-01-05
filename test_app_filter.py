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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
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
Created on Nov 24, 2010
'''

from selenium import selenium
import vars
import unittest

import feedback_page
import search_results_page


class SearchFirefox(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(vars.ConnectionParameters.server, vars.ConnectionParameters.port,
                                vars.ConnectionParameters.browser, vars.ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(vars.ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_that_app_filter_versions_exist(self):
        """
            this tc covers tc # 13601 & 13602 in litmus
            1. verifies product=<name>&version=<num> in the url
            2. verifies all the Fx/Mobile versions exists in
               the search filters
        """
        sel = self.selenium
        feedback_obj        = feedback_page.FeedbackPage(sel)
        search_page_obj     = search_results_page.SearchResultsPage(sel)

        feedback_obj.go_to_feedback_page()
        feedback_obj.select_prod_firefox()
        feedback_obj.select_firefox_version('b7')
        search_page_obj.verify_firefox_search_page_url()

        feedback_obj.select_firefox_version('b6')
        search_page_obj.verify_firefox_search_page_url()

        feedback_obj.go_to_feedback_page()
        feedback_obj.select_prod_mobile()
        feedback_obj.select_mobile_version('4.0b2')
        search_page_obj.verify_mobile_search_page_url()

        feedback_obj.select_mobile_version('4.0b1')
        search_page_obj.verify_mobile_search_page_url()

        feedback_obj.go_to_feedback_page()
        feedback_obj.select_prod_firefox()
        feedback_obj.verify_all_firefox_versions()

        feedback_obj.go_to_feedback_page()
        feedback_obj.select_prod_mobile()
        feedback_obj.verify_all_mobile_versions()

    def test_that_search_page_results_match_search_query(self):
        """
            this tc covers tc # 13603 & 13604 in litmus
            verifies:
            product=firefox in <input type="hidden" value="firefox" name="product">
            and
            version=4.0b6 in <input type="hidden" value="4.0b6" name="version">
        """
        sel = self.selenium
        feedback_obj        = feedback_page.FeedbackPage(sel)
        search_page_obj     = search_results_page.SearchResultsPage(sel)

        feedback_obj.go_to_feedback_page()
        for ver in feedback_obj._fx_versions:
            feedback_obj.select_prod_firefox()
            feedback_obj.select_firefox_version(ver)
            search_page_obj.verify_search_form_prod_ver(feedback_obj._app_name_fx, ver)

        feedback_obj.go_to_feedback_page()
        for ver in feedback_obj._mobile_versions:
            feedback_obj.select_prod_mobile()
            feedback_obj.select_mobile_version(ver)
            search_page_obj.verify_search_form_prod_ver(feedback_obj._app_name_mb, ver)

if __name__ == "__main__":
    unittest.main()
