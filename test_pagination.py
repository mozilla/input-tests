#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *****BEGIN LICENSE BLOCK *****
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


from selenium import selenium
import vars
import unittest

import themes_page
import search_results_page


class TestPagination(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(vars.ConnectionParameters.server, vars.ConnectionParameters.port, vars.ConnectionParameters.browser, vars.ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(vars.ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_filters_persist_when_paging_through_results(self):
        """

        This testcase covers # 1508 in Litmus
        1. Verifies the filter is in the URL
        2. Verifies the currently applied filter is styled appropriately
        3. Verifies the currently results of the filter

        """
        selenium = self.selenium
        themes_page_obj = themes_page.ThemesPage(selenium)
        search_results_page_obj = search_results_page.SearchResultsPage(selenium)
        
        themes_page_obj.go_to_themes_page()
        themes_page_obj.click_type_issues()
        themes_page_obj.click_next_page()
        self.assertEqual(search_results_page_obj.type_from_url, "sad")
        self.assertEqual(themes_page_obj.current_type, "Issues")
        self.assertEqual(themes_page_obj.praise_count, 0)

if __name__ == "__main__":
    unittest.main()
