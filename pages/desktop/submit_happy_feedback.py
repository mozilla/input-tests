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

from pages.desktop.submit_feedback import SubmitFeedbackPage


class SubmitHappyFeedbackPage(SubmitFeedbackPage):

    _feedback_locator = (By.ID, 'happy-description')
    _remaining_character_count_locator = (By.ID, 'happy-description-counter')
    _submit_feedback_locator = (By.CSS_SELECTOR, '#happy-submit a')
    _error_locator = (By.CSS_SELECTOR, '#happy .errorlist li')
    _back_locator = (By.CSS_SELECTOR, '#happy > header > nav > a')

    def go_to_submit_happy_feedback_page(self):
        self.selenium.get(self.base_url + '/feedback#happy')
        self.is_the_current_page

    def is_visible(self):
        return self.is_element_visible(self._happy_page_locator)
