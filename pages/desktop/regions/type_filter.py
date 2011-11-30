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
#   Bebe <Florin.strugariu@softvision.ro>
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

from page import Page


class TypeFilter(Page):

    class ButtonFilter(Page):

        _selected_type_locator = (By.CSS_SELECTOR, '#filter_type a.selected')
        _all_locator = (By.CSS_SELECTOR, '#filter_type li:nth-child(1) a')
        _praise_locator = (By.CSS_SELECTOR, '#filter_type li:nth-child(2) a')
        _issues_locator = (By.CSS_SELECTOR, '#filter_type li:nth-child(3) a')
        _ideas_locator = (By.CSS_SELECTOR, '#filter_type li:nth-child(4) a')

        @property
        def selected_type(self):
            return self.selenium.find_element(*self._selected_type_locator).text

        def click_issues(self):
            self.selenium.find_element(*self._issues_locator).click()


    class CheckboxFilter(Page):

        _types_locator = (By.CSS_SELECTOR, '#filter_type li')

        @property
        def types(self):
            return [self.Type(self.testsetup, element) for element in self.selenium.find_elements(*self._types_locator)]

        class Type(Page):

            _checkbox_locator = (By.TAG_NAME, 'input')
            _name_locator = (By.CSS_SELECTOR, 'label > strong')
            _message_count_locator = (By.CLASS_NAME, 'count')
            _percent_locator = (By.CLASS_NAME, 'perc')

            def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self._root_element = element

            @property
            def is_selected(self):
                return self._root_element.find_element(*self._checkbox_locator).is_checked()

            @property
            def name(self):
                return self._root_element.find_element(*self._name_locator).text

            @property
            def message_count(self):
                return self._root_element.find_element(*self._message_count_locator).text

            @property
            def percent(self):
                return self._root_element.find_element(*self._percent_locator).text

            def select(self):
                return self._root_element.find_element(*self._checkbox_locator).click
