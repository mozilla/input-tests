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

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base import BasePage


class SubmitFeedbackPage(BasePage):

    _page_title = 'Submit Feedback :: Firefox Input'

    _idea_page_locator = (By.ID, 'idea')
    _happy_page_locator = (By.ID, 'happy')
    _sad_page_locator = (By.ID, 'sad')
    _intro_page_locator = (By.ID, 'intro')

    _idea_button_locator = (By.ID, 'intro-idea')
    _happy_button_locator = (By.ID, 'intro-happy')
    _sad_button_locator = (By.ID, 'intro-sad')

    _support_page_locator = (By.LINK_TEXT, 'Firefox Support')

    def go_to_submit_feedback_page(self):
        self.selenium.get(self.base_url + '/feedback/')
        self.is_the_current_page

    def type_feedback(self, feedback):
        self.selenium.find_element(*self._feedback_locator).send_keys(feedback)

    def click_support_page(self):
        self.selenium.find_element(*self._support_page_locator).click()

    def wait_for_page_to_slide_into_view(self, page_locator):
        WebDriverWait(self.selenium, 3).until(lambda s: 'entering' in s.find_element(*page_locator).get_attribute('class'))
        WebDriverWait(self.selenium, 3).until(lambda s: 'entering' not in s.find_element(*page_locator).get_attribute('class'))

    def click_happy_feedback(self):
        self.selenium.find_element(*self._happy_button_locator).click()
        self.wait_for_page_to_slide_into_view(self._happy_page_locator)
        from pages.desktop.submit_happy_feedback import SubmitHappyFeedbackPage
        return SubmitHappyFeedbackPage(self.testsetup)

    def click_sad_feedback(self):
        self.selenium.find_element(*self._sad_button_locator).click()
        self.wait_for_page_to_slide_into_view(self._sad_page_locator)
        from pages.desktop.submit_sad_feedback import SubmitSadFeedbackPage
        return SubmitSadFeedbackPage(self.testsetup)

    def click_idea_feedback(self):
        self.selenium.find_element(*self._idea_button_locator).click()
        self.wait_for_page_to_slide_into_view(self._idea_page_locator)
        from pages.desktop.submit_idea import SubmitIdeaPage
        return SubmitIdeaPage(self.testsetup)

    def click_back(self):
        self.selenium.find_element(*self._back_locator).click()

    @property
    def support_page_link_address(self):
        return self.selenium.find_element(*self._support_page_locator).get_attribute('href')

    @property
    def error_message(self):
        return self.selenium.find_element(*self._error_locator).text

    @property
    def remaining_character_count(self):
        return self.selenium.find_element(*self._remaining_character_count_locator).text

    @property
    def is_remaining_character_count_limited(self):
        css_class = self.selenium.find_element(*self._remaining_character_count_locator).get_attribute('class')
        return 'limited-characters-remaining' in css_class and not 'no-characters-remaining' in css_class

    @property
    def is_remaining_character_count_negative(self):
        return 'no-characters-remaining' in self.selenium.find_element(*self._remaining_character_count_locator).get_attribute('class')

    @property
    def is_submit_feedback_enabled(self):
        return not 'disabled' in self.selenium.find_element(*self._submit_feedback_locator).get_attribute('class')

    def submit_feedback(self, expected_result='success'):
        self.selenium.find_element(*self._submit_feedback_locator).click()
        if expected_result == 'success':
            from pages.desktop.thanks import ThanksPage
            return ThanksPage(self.testsetup)
