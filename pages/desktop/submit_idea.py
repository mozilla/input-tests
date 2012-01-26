#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.desktop.submit_feedback import SubmitFeedbackPage


class SubmitIdeaPage(SubmitFeedbackPage):

    _feedback_locator = (By.ID, 'idea-description')
    _remaining_character_count_locator = (By.ID, 'idea-description-counter')
    _submit_feedback_locator = (By.CSS_SELECTOR, '#idea-submit a')
    _error_locator = (By.CSS_SELECTOR, '#idea .errorlist li')
    _back_locator = (By.CSS_SELECTOR, '#idea > header > nav > a')

    def go_to_submit_idea_page(self):
        self.selenium.get(self.base_url + '/feedback#idea')
        self.is_the_current_page

    def is_visible(self):
        return self.is_element_visible(self._idea_page_locator)
