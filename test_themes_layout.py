#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *****BEGIN LICENSE BLOCK *****
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
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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

from selenium import selenium
from vars import ConnectionParameters
import unittest
import themes_page

class TestThemes(unittest.TestCase):


    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    def test_the_heder_layout(self):
        """
        Litmus 13722 - input:Verify the layout of Themes page(Themes tab)
        """
        themes = themes_page.ThemesPage(self.selenium)
        themes.go_to_themes_page()

        self.assertTrue(themes.is_element_visible(themes.firefox_link))
        self.assertEqual(themes.get_atribute(themes.firefox_link, "href"),
                        "/en-US/")
        themes.click_and_check(themes.firefox_link, "Welcome :: Firefox Input")
        themes.go_back()

        self.assertTrue(themes.is_element_visible(themes.themes_link))
        self.assertEqual(themes.get_atribute(themes.themes_link, "href"),
                         "/en-US/themes")
        themes.click_and_check(themes.themes_link, "Themes :: Firefox Input")

        self.assertTrue(themes.is_element_visible(themes.feedback_link))
        self.assertEqual(themes.get_atribute(themes.feedback_link, "href"),
                         "/en-US/")
        themes.click_and_check(themes.feedback_link, "Welcome :: Firefox Input")
        themes.go_back()

        self.assertTrue(themes.is_element_visible(themes.sites_link))
        self.assertEqual(themes.get_atribute(themes.sites_link, "href"),
                         "/en-US/sites")
        themes.click_and_check(themes.sites_link, "Sites :: Firefox Input")
        themes.go_back()

    def test_product_and_type_filter(self):

        themes = themes_page.ThemesPage(self.selenium)
        themes.go_to_themes_page()

        products = themes.product_filter.products()

        for p in products:
            p.select()
            self.assertTrue(p.is_selected)
            self.assertTrue(themes.contains_item(themes.product_list, p.name))


        types = themes.type_filter.types()
        for t in types:
            t.select()
            self.assertTrue(t.is_selected)
            self.assertTrue(themes.contains_item(themes.type_list, t.name))

    def test_themes_section(self):

        themes = themes_page.ThemesPage(self.selenium)
        themes.go_to_themes_page()

        self.assertEqual(themes.messages_title, "Common Themes")
        self.assertNotEqual(themes.theme_count , 0)

if __name__ == "__main__":
    unittest.main()

