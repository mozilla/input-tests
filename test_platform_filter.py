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
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
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
from vars import ConnectionParameters
import unittest

import feedback_page


class TestPlatformFilter(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_feedback_can_be_filtered_by_platform(self):
        """
        This testcase covers # 15215 in Litmus
        1. Verify that the selected platform is the only one to appear in the list and is selected
        2. Verify that the number of messages in the platform list matches the number of messages returned
        3. Verify that the platform appears in the URL
        4. Verify that the platform for all messages on the first page of results is correct
        """
        feedback_pg = feedback_page.FeedbackPage(self.selenium)

        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product('firefox')
        feedback_pg.product_filter.select_version('--')

        platform_name = "Mac OS X"
        platform = feedback_pg.platform_filter.platform(platform_name)
        platform_message_count = platform.message_count
        platform_code = platform.code
        platform.select()

        self.assertEqual(feedback_pg.platform_filter.platform_count, 1)
        self.assertTrue(platform.is_selected)
        self.assertEqual(feedback_pg.total_message_count.replace(',', ''), platform_message_count)
        self.assertEqual(feedback_pg.platform_from_url, platform_code)
        [self.assertEqual(message.platform, platform_name) for message in feedback_pg.messages]

if __name__ == "__main__":
    unittest.main()
