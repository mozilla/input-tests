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
'''
Created on Feb 24, 2011
'''
from page import Page


class LocaleFilter(Page):

    _all_locales_locator = "id('filter_locale')//div/li"
    _initial_locales_locator = "id('filter_locale')//div[not(@class='extra')]/li"
    _more_locales_link_locator = "css=#filter_locale .more"
    _extra_locales_locator = "css=#filter_locale .extra"
    _total_message_count_locator = "css=#filter_locale .bars"

    @property
    def total_message_count(self):
        return self.selenium.get_attribute(self._total_message_count_locator + "@data-total")

    @property
    def is_extra_locales_visible(self):
        return self.selenium.is_visible(self._extra_locales_locator)

    @property
    def locale_count(self):
        if self.is_extra_locales_visible:
            return int(self.selenium.get_xpath_count(self._all_locales_locator))
        else:
            return int(self.selenium.get_xpath_count(self._initial_locales_locator))

    def show_extra_locales(self):
        self.selenium.click(self._more_locales_link_locator)
        self.wait_for_element_not_visible(self._more_locales_link_locator)
        self.wait_for_element_visible(self._extra_locales_locator)

    def contains_locale(self, lookup):
        try :
            self.selenium.get_text("css=#filter_locale div li:contains(%s)" % lookup)
            return True
        except :
            return False

    def locales(self):
        res = []
        for i in range(self.locale_count):
            if i != 16:
                res.append(self.Locale(self.testsetup, i))
        return res

    def locale(self, lookup):
        return self.Locale(self.testsetup, lookup)

    class Locale(Page):

        _checkbox_locator = " input"
        _name_locator = " label > strong"
        _message_count_locator = " .count"
        _message_percentage_locator = " .perc"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "css=#filter_locale div li:nth(" + str(self.lookup) + ")"
            else:
                # lookup by name
                return "css=#filter_locale li:contains(" + self.lookup + ")"

        @property
        def is_selected(self):
            return self.selenium.is_checked(self.absolute_locator(self._checkbox_locator))

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        @property
        def code(self):
            return self.selenium.get_attribute(self.absolute_locator(self._checkbox_locator + "@value"))

        @property
        def message_count(self):
            return self.selenium.get_text(self.absolute_locator(self._message_count_locator))

        @property
        def message_percentage(self):
            return self.selenium.get_text(self.absolute_locator(self._message_percentage_locator))

        def select(self):
            self.selenium.click(self.absolute_locator(self._checkbox_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

        def percentage(self, total_messages):
                return round((float(self.message_count) / float(total_messages)) * 100)
