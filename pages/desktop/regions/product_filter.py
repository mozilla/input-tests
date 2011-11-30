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
from selenium.webdriver.support.select import Select

from page import Page


class ProductFilter(Page):

    class ComboFilter(Page):

        _product_dropdown_locator = (By.ID, 'product')
        _version_dropdown_locator = (By.ID, 'version')

        @property
        def products(self):
            """Returns a list of available products."""
            select = Select(self.selenium.find_element(*self._product_dropdown_locator))
            return [option.get_attribute('value') for option in select.options]

        @property
        def selected_product(self):
            """Returns the currently selected product."""
            return Select(self.selenium.find_element(*self._product_dropdown_locator)).first_selected_option.get_attribute('value')

        def select_product(self, product):
            """Selects a product."""
            if not product == self.selected_product:
                Select(self.selenium.find_element(*self._product_dropdown_locator)).select_by_value(product)

        @property
        def versions(self):
            """Returns a list of available versions."""
            select = Select(self.selenium.find_element(*self._version_dropdown_locator))
            return [option.get_attribute('value') for option in select.options]

        @property
        def selected_version(self):
            """Returns the currently selected product version."""
            return Select(self.selenium.find_element(*self._version_dropdown_locator)).first_selected_option.get_attribute('value')

        def select_version(self, version):
            """Selects a product version."""
            select = Select(self.selenium.find_element(*self._version_dropdown_locator))

            if type(version) == int:
                select.select_by_index(version)
            else:
                select.select_by_value(version)
