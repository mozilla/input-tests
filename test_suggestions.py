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

Created on Dec 22, 2010

'''

from selenium import selenium
import vars
import unittest

import suggestion_page


class SubmitSuggestion(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(vars.ConnectionParameters.server, vars.ConnectionParameters.port, vars.ConnectionParameters.browser, vars.ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(vars.ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_remaining_character_count(self):
        """

        This testcase covers # 15029 in Litmus
        1. Verifies the remaining character count decreases
        2. Verifies that the remaining character count style changes at certain thresholds
        3. Verified that the 'Submit Feedback' button is disabled when character limit is exceeded

        """
        sel = self.selenium
        suggestion_page_obj = suggestion_page.SuggestionPage(sel)

        suggestion_page_obj.go_to_suggestion_page()
        self.assertEqual(suggestion_page_obj.remaining_character_count, "250")
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_low)
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_very_low)
        self.assertTrue(suggestion_page_obj.is_submit_feedback_enabled)

        suggestion_page_obj.set_suggestion("a"*199)
        self.assertEqual(suggestion_page_obj.remaining_character_count, "51")
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_low)
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_very_low)
        self.assertTrue(suggestion_page_obj.is_submit_feedback_enabled)

        suggestion_page_obj.set_suggestion("b"*1)
        self.assertEqual(suggestion_page_obj.remaining_character_count, "50")
        self.assertTrue(suggestion_page_obj.is_remaining_character_count_low)
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_very_low)
        self.assertTrue(suggestion_page_obj.is_submit_feedback_enabled)

        suggestion_page_obj.set_suggestion("c"*24)
        self.assertEqual(suggestion_page_obj.remaining_character_count, "26")
        self.assertTrue(suggestion_page_obj.is_remaining_character_count_low)
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_very_low)
        self.assertTrue(suggestion_page_obj.is_submit_feedback_enabled)

        suggestion_page_obj.set_suggestion("d"*1)
        self.assertEqual(suggestion_page_obj.remaining_character_count, "25")
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_low)
        self.assertTrue(suggestion_page_obj.is_remaining_character_count_very_low)
        self.assertTrue(suggestion_page_obj.is_submit_feedback_enabled)

        suggestion_page_obj.set_suggestion("e"*25)
        self.assertEqual(suggestion_page_obj.remaining_character_count, "0")
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_low)
        self.assertTrue(suggestion_page_obj.is_remaining_character_count_very_low)
        self.assertTrue(suggestion_page_obj.is_submit_feedback_enabled)

        suggestion_page_obj.set_suggestion("f"*1)
        self.assertEqual(suggestion_page_obj.remaining_character_count, "-1")
        self.assertFalse(suggestion_page_obj.is_remaining_character_count_low)
        self.assertTrue(suggestion_page_obj.is_remaining_character_count_very_low)
        # Assert disabled for Bug 616230
        #self.assertFalse(suggestion_page_obj.is_submit_feedback_enabled)

if __name__ == "__main__":
    unittest.main()
