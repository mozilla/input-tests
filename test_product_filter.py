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
#                 Dave Hunt <dhunt@mozilla.com>
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
from vars import ConnectionParameters
import unittest

import feedback_page
import sites_page
import search_results_page


class SearchFirefox(unittest.TestCase):

    _products = (
        {"name": "firefox", "versions": ("4.0b10", "4.0b9", "4.0b8", "4.0b7", "4.0b6", "4.0b5", "4.0b4", "4.0b3", "4.0b2", "4.0b1")},
        {"name": "mobile", "versions": ("4.0b4", "4.0b3", "4.0b2", "4.0b1")}
    )

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_feedback_can_be_filtered_by_all_expected_products_and_versions(self):
        """

        This testcase covers # 13601, 13602, 13603 & 13604 in Litmus
        1. Verify the correct products exist
        2. Verify the correct product versions exist
        3. Verify that each of the versions return results
        4. Verify that the state of the filters are correct after being applied
        5. Verify product and version values in the URL

        """
        sel = self.selenium
        feedback_pg = feedback_page.FeedbackPage(sel)
        search_results_pg = search_results_page.SearchResultsPage(sel)

        feedback_pg.go_to_feedback_page()
        self.assertEqual(len(feedback_pg.products), len(self._products))
        for product in self._products:
            feedback_pg.select_product(product["name"])
            versions = list(product["versions"])
            # Add an empty version so we can check the filter for all versions of the current product
            versions.insert(0, "")
            self.assertEqual(len(feedback_pg.versions), len(versions))
            for version in versions:
                print "Checking product '%s' and version '%s'." % (product["name"], version)
                feedback_pg.select_version(version)
                self.assertEqual(feedback_pg.selected_product, product["name"])
                self.assertEqual(feedback_pg.selected_version, version)
                self.assertEqual(search_results_pg.product_from_url, product["name"])
                self.assertEqual(search_results_pg.version_from_url, version)

    def test_sites_can_be_filtered_by_all_expected_products_and_versions(self):
        """

        This testcase covers # 15042, 15043, 15044 & 15045 in Litmus
        1. Verify the correct products exist
        2. Verify the correct product versions exist
        3. Verify that each of the versions return results
        4. Verify that the state of the filters are correct after being applied
        5. Verify product and version values in the URL

        """
        sel = self.selenium
        sites_pg = sites_page.SitesPage(sel)
        search_results_pg = search_results_page.SearchResultsPage(sel)

        sites_pg.go_to_sites_page()
        self.assertEqual(len(sites_pg.products), len(self._products))
        for product in self._products:
            sites_pg.select_product(product["name"])
            versions = list(product["versions"])
            self.assertEqual(len(sites_pg.versions), len(versions))
            # Reverse version order because latest version is selected by default
            versions.reverse()
            for version in versions:
                print "Checking product '%s' and version '%s'." % (product["name"], version)
                sites_pg.select_version(version)
                self.assertEqual(sites_pg.selected_product, product["name"])
                self.assertEqual(sites_pg.selected_version, version)
                self.assertEqual(search_results_pg.product_from_url, product["name"])
                self.assertEqual(search_results_pg.version_from_url, version)

if __name__ == "__main__":
    unittest.main()
