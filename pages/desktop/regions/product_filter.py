#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
