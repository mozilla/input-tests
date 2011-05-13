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
Created on Mar 25, 2011
'''
from page import Page


class ProductFilter(Page):

    class ComboFilter(Page):

        _product_dropdown_locator = "id=product"
        _version_dropdown_locator = "id=version"

        @property
        def products(self):
            """
            returns a list of available products
            """
            return self.selenium.get_select_options(self._product_dropdown_locator)

        @property
        def selected_product(self):
            """
            returns the currently selected product
            """
            self.wait_for_element_present(self._product_dropdown_locator)
            return self.selenium.get_selected_value(self._product_dropdown_locator)

        def select_product(self, product):
            """
            selects product
            """
            if not product == self.selected_product:
                self.selenium.select(self._product_dropdown_locator, "value=%s" % product)
                self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def versions(self):
            """
            returns a list of available versions
            """
            return self.selenium.get_select_options(self._version_dropdown_locator)

        def selected_version(self, type='value'):
            """
            returns the currently selected product version
            """
            return getattr(self.selenium, "get_selected_" + type)(self._version_dropdown_locator)

        def select_version(self, lookup, by='value'):
            """
            selects product version
            """
            if not lookup == self.selected_version(by):
                self.selenium.select(self._version_dropdown_locator, "%s=%s" % (by, lookup))
                self.selenium.wait_for_page_to_load(self.timeout)
