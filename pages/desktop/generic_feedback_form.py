#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import BasePage


class GenericFeedbackFormPage(BasePage):

    _page_title = 'Submit Your Feedback :: Firefox Input'

    _intro_card_locator = (By.ID, 'intro')

    _happy_button_locator = (By.CSS_SELECTOR, '#buttons button.happy')
    _sad_button_locator = (By.CSS_SELECTOR, '#buttons button.sad')

    _moreinfo_card_locator = (By.ID, 'moreinfo')
    _description_locator = (By.ID, 'description')
    _url_locator = (By.ID, 'id_url')
    _moreinfo_character_count_locator = (By.ID, 'description-counter')
    _moreinfo_back_locator = (By.CSS_SELECTOR, '#moreinfo button.back')
    _moreinfo_next_locator = (By.ID, 'description-next-btn')

    _email_card_locator = (By.ID, 'email')
    _email_checkbox_locator = (By.ID, 'email-ok')
    _email_locator = (By.ID, 'id_email')
    _email_back_locator = (By.CSS_SELECTOR, '#email button.back')

    _submit_locator = (By.ID, 'form-submit-btn')

    _support_page_locator = (By.LINK_TEXT, 'Firefox Support')

    def go_to_feedback_page(self):
        self.selenium.get(self.base_url + '/feedback/')
        self.is_the_current_page

    def type_feedback(self, feedback):
        self.selenium.find_element(*self._feedback_locator).send_keys(feedback)

    def click_support_page(self):
        self.selenium.find_element(*self._support_page_locator).click()

    def wait_for(self, locator):
        # FIXME: self.timeout
        WebDriverWait(self.selenium, 5).until(EC.visibility_of_element_located(locator))

    def click_happy_feedback(self):
        self.selenium.find_element(*self._happy_button_locator).click()
        self.wait_for(self._description_locator)

    def click_sad_feedback(self):
        self.selenium.find_element(*self._sad_button_locator).click()
        self.wait_for(self._description_locator)

    def click_moreinfo_back(self):
        self.selenium.find_element(*self._moreinfo_back_locator).click()
        self.wait_for(self._happy_button_locator)

    def set_description(self, text, send_keys=True):
        """Sets the value of the description textarea

        :arg text: The text to set

        :arg setvalue: Whether or not to use send_keys. The problem is
            that send_keys takes a crazy amount of time for texts >
            200 characters. So if send_keys is False, then we jam it
            in with execute_script.

        """
        desc = self.selenium.find_element(*self._description_locator)
        if send_keys:
            desc.send_keys(text)
        else:
            text = text.replace("'", "\\'").replace('"', '\\"')
            self.selenium.execute_script("$('#description').val('" + text + "')")

    def set_url(self, text):
        url = self.selenium.find_element(*self._url_locator)
        url.clear()
        url.send_keys(text)

    def click_moreinfo_next(self):
        self.selenium.find_element(*self._moreinfo_next_locator).click()
        self.wait_for(self._email_checkbox_locator)

    def click_email_back(self):
        self.selenium.find_element(*self._email_back_locator).click()
        self.wait_for(self._description_locator)

    def check_email_checkbox(self, checked=True):
        checkbox = self.selenium.find_element(*self._email_checkbox_locator)
        if checked != checkbox.is_selected():
            checkbox.click()

    def set_email(self, text):
        email = self.selenium.find_element(*self._email_locator)
        email.clear()
        email.send_keys(text)

    def submit(self, expect_success=True):
        self.selenium.find_element(*self._submit_locator).click()
        if expect_success:
            from pages.desktop.thanks import ThanksPage
            return ThanksPage(self.testsetup)

    @property
    def support_page_link_address(self):
        return self.selenium.find_element(*self._support_page_locator).get_attribute('href')

    @property
    def is_moreinfo_next_enabled(self):
        return self.selenium.find_element(*self._moreinfo_next_locator).is_enabled()

    @property
    def is_url_valid(self):
        return not 'invalid' in self.selenium.find_element(*self._url_locator).get_attribute('class')

    @property
    def is_email_valid(self):
        return not 'invalid' in self.selenium.find_element(*self._email_locator).get_attribute('class')

    @property
    def error_message(self):
        return self.selenium.find_element(*self._error_locator).text

    @property
    def remaining_character_count(self):
        return int(self.selenium.find_element(*self._moreinfo_character_count_locator).text)

    @property
    def is_submit_feedback_enabled(self):
        return not 'disabled' in self.selenium.find_element(*self._submit_feedback_locator).get_attribute('class')
