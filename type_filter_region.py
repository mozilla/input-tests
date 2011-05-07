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
#                 Soren Jones
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
Created on Mar 24, 2011
'''
from page import Page
from vars import ConnectionParameters

page_load_timeout = ConnectionParameters.page_load_timeout


class TypeFilter(Page):

    class ButtonFilter(object):

        _selected_type_locator = "css=#filter_type a.selected"

        @property
        def selected_type(self):
            return self.selenium.get_text(self._selected_type_locator)

        def select_type(self, type):
            self.selenium.click("css=#filter_type a:contains(%s)" % type)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    class FilterOption(object):

        _chart_locator = "css=svg g:nth-child(8) > * tspan"
        _name_locator = " > label strong"
        _root_locator = "css=#filter_type li"

        def __init__(self, selenium, index):
            self.selenium = selenium
            self.index = index

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def chart_locator(self):
            """

            Returns the locator for the specified type name in the chart legend

            """
            return self._chart_locator + ":contains(%s)" % (self.name)

        @property
        def name(self):
            """

            Returns the name of a feedback type in the Feedback by Type filter bar

            """
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        @property
        def root_locator(self):
            """

            Returns the locator for the nth type name in the Feedback by Type filter bar

            """
            return self._root_locator + ":nth-child(%s)" % (self.index)
