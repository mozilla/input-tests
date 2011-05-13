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
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#                 Matt Brandt <mbrandt@mozilla.com>
#                 Bob Silverberg <bob.silverberg@gmail.com>
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
Created on Jan 28, 2011
'''
import input_base_page
import thanks_page
import vars

page_load_timeout = vars.ConnectionParameters.page_load_timeout


class SubmitFeedbackPage(input_base_page.InputBasePage):

    _page_title = u'Submit Feedback :: Firefox Input'

    _idea_page_locator = 'id=idea'
    _happy_page_locator = 'id=happy'

    def set_feedback(self, feedback):
        self.selenium.type_keys(self._feedback_locator, feedback)
        self.selenium.key_up(self._feedback_locator, feedback[-1:])

    @property
    def error_message(self):
        self.wait_for_element_visible(self._error_locator)
        return self.selenium.get_text(self._error_locator)

    @property
    def remaining_character_count(self):
        return self.selenium.get_text(self._remaining_character_count_locator)

    @property
    def is_remaining_character_count_low(self):
        try:
            return self.selenium.is_visible(self._remaining_character_count_locator + ".low")
        except:
            return False

    @property
    def is_remaining_character_count_very_low(self):
        try:
            return self.selenium.is_visible(self._remaining_character_count_locator + ".verylow")
        except:
            return False

    def submit_feedback(self, expected_result='success'):
        self.selenium.click(self._submit_feedback_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)
        if expected_result == 'success':
            return thanks_page.ThanksPage(self.selenium)
        else:
            self.wait_for_element_visible(self._error_locator)
