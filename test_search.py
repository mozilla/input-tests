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
# Contributor(s): David Burns
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


from selenium import selenium
from vars import ConnectionParameters
import unittest

import beta_feedback_page


class TestSearch(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_that_empty_search_of_beta_feedback_returns_some_data(self):
        '''
            Litmus 13847
        '''
        beta_feedback_pg = beta_feedback_page.BetaFeedbackPage(self.selenium)

        beta_feedback_pg.go_to_beta_feedback_page()
        beta_feedback_pg.search_for('')
        self.assertTrue(0 < beta_feedback_pg.message_count)

    def test_that_we_can_search_beta_feedback_with_unicode(self):
        '''
            Litmus 13697
        '''
        beta_feedback_pg = beta_feedback_page.BetaFeedbackPage(self.selenium)

        beta_feedback_pg.go_to_beta_feedback_page()
        beta_feedback_pg.search_for(u"Tension et violence en C\xf4ted'Ivoire avant les r\xe9sultats")
        self.assertTrue(0 < beta_feedback_pg.message_count)

if __name__ == "__main__":
    unittest.main()
