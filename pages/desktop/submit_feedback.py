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
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla.
#
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Dave Hunt <dhunt@mozilla.com>
#   Matt Brandt <mbrandt@mozilla.com>
#   Bob Silverberg <bob.silverberg@gmail.com>
#   Bebe <florin.strugariu@softvision.ro>
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

from pages.base import BasePage


class SubmitFeedbackPage(BasePage):

    _page_title = 'Submit Feedback :: Firefox Input'

    _idea_page_locator = 'id=idea'
    _happy_page_locator = 'id=happy'
    _sad_page_locator = 'id=sad'
    _intro_page_locator = 'id=intro'

    _idea_button_locator = 'id=intro-idea'
    _happy_button_locator = 'id=intro-happy'
    _sad_button_locator = 'id=intro-sad'

    _support_page_locator = 'link=Firefox Support'

    def go_to_submit_feedback_page(self):
        self.selenium.open('/feedback/')
        self.is_the_current_page

    def set_feedback(self, feedback):
        self.selenium.type_keys(self._feedback_locator, feedback)
        self.selenium.key_up(self._feedback_locator, feedback[-1:])

    def click_support_page(self):
        self.selenium.click(self._support_page_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_happy_feedback(self):
        self.selenium.click(self._happy_button_locator)
        self.wait_for_click_to_finish_animating('happy')
        from pages.desktop.submit_happy_feedback import SubmitHappyFeedbackPage
        return SubmitHappyFeedbackPage(self.testsetup)

    def click_sad_feedback(self):
        self.selenium.click(self._sad_button_locator)
        self.wait_for_click_to_finish_animating('sad')
        from pages.desktop.submit_sad_feedback import SubmitSadFeedbackPage
        return SubmitSadFeedbackPage(self.testsetup)

    def click_idea_feedback(self):
        self.selenium.click(self._idea_button_locator)
        self.wait_for_click_to_finish_animating('idea')
        from pages.desktop.submit_idea import SubmitIdeaPage
        return SubmitIdeaPage(self.testsetup)

    def click_back(self):
        self.selenium.click(self._back_locator)
        self.wait_for_click_to_finish_animating('intro')

    def wait_for_click_to_finish_animating(self, locator):
        self.selenium.wait_for_condition(
           "selenium.browserbot.getCurrentWindow().document.getElementById('" + locator + "').className == 'entering'", 10000)
        self.selenium.wait_for_condition(
           "selenium.browserbot.getCurrentWindow().document.getElementById('" + locator + "').className == ''", 10000)

    def suport_page_link_address(self):
        return self.selenium.get_attribute('%s@href' % self._support_page_locator)

    @property
    def error_message(self):
        self.wait_for_element_visible(self._error_locator)
        return self.selenium.get_text(self._error_locator)

    @property
    def remaining_character_count(self):
        return self.selenium.get_text(self._remaining_character_count_locator)

    @property
    def is_remaining_character_count_limited(self):
        try:
            return self.selenium.is_visible(self._remaining_character_count_locator + ".limited-characters-remaining:not(.no-characters-remaining)")
        except:
            return False

    @property
    def is_remaining_character_count_negative(self):
        try:
            return self.selenium.is_visible(self._remaining_character_count_locator + ".no-characters-remaining")
        except:
            return False

    def submit_feedback(self, expected_result='success'):
        self.selenium.click(self._submit_feedback_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        if expected_result == 'success':
            from pages.desktop.thanks import ThanksPage
            return ThanksPage(self.testsetup)
        else:
            self.wait_for_element_visible(self._error_locator)
