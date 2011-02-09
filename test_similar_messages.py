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
'''
Created on Jan 26, 2011
'''

from selenium import selenium
from vars import ConnectionParameters
import unittest

import beta_sites_page
import search_results_page


class TestSimilarMessages(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_similar_messages(self):
        """

        This testcase covers # 13807 in Litmus

        """
        beta_sites_pg = beta_sites_page.BetaSitesPage(self.selenium)
        results_pg = search_results_page.SearchResultsPage(self.selenium)

        beta_sites_pg.go_to_beta_sites_page()
        beta_sites_pg.select_product('firefox')
        beta_sites_pg.select_version(1, by='index')

        selected_site = beta_sites_pg.site_url(1)
        beta_sites_pg.click_site(selected_site, by='url')
        beta_sites_pg.click_first_similar_messages_link()
        beta_sites_pg.click_next_page()

        self.assertEqual(beta_sites_pg.messages_heading, 'Theme')
        self.assertEqual(results_pg.page_from_url, '2')
        self.assertEqual(beta_sites_pg.theme_callout, 'Theme for ' + selected_site)
        self.assertTrue(0 < beta_sites_pg.message_count)
        self.assertEqual(beta_sites_pg.back_link, 'Back to ' + selected_site + u' \xbb')
        self.assertTrue(selected_site in beta_sites_pg.first_message_url)

if __name__ == "__main__":
    unittest.main()
