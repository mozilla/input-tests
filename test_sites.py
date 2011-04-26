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
from pip.locations import site_packages

"""
Litmus 13644 - Input: Verify that secure/SSL/HTTPS URLs in Sites have (SSL) to the right of their URLs
"""

from selenium import selenium
from vars import ConnectionParameters
import unittest
import pytest
xfail = pytest.mark.xfail

#import release_sites
import sites_page

class TestSites(unittest.TestCase):

    _products = (
                 {"name": "firefox", "versions": ("-- all --", "6.0a1", "5.0a2", "4.0", "4.0b12")},
                 {"name": "mobile", "versions": ("-- all --", "4.0", "4.0b5", "4.0b4", "4.0b3", "4.0b2", "4.0b1")}
                  )

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    """
    Litmus 13644 - Input: Verify that secure/SSL/HTTPS URLs in Sites have (SSL) to the right of their URLs
    """
    def test_ssh(self):
        
        site_page = sites_page.SitesPage(self.selenium)
        site_page.go_to_sites_page()

        for product in  site_page.product_filter.products:
            site_page.product_filter.select_product(product.lower())
            for version in site_page.product_filter.versions:
                if version != "-- all --":
                    site_page.product_filter.select_version(version)
                    if site_page.site_count != 0:
                        for site in  site_page.sites:
                            if "https" in site.url:
                                self.assertTrue(site.is_ssh)



    
    """
    Litmus 13718 - input:Verify Product controls in sites homepage
    """
    def test_products_values(self):
        
        site_page = sites_page.SitesPage(self.selenium)
        site_page.go_to_sites_page()
        
        products = site_page.product_filter.products
        self.assertEqual(products[0],"Firefox")
        self.assertEqual(products[1],"Mobile")



    """
    Litmus 13723 - input:Verify the layout of Sites page(Sites tab)
    """
    
    def test_the_heder_layout(self):
        sites = sites_page.SitesPage(self.selenium)
        sites.go_to_sites_page()

        self.assertTrue(sites.is_element_visible(sites.get_firefox_link))
        self.assertEqual(sites.get_atribute(sites.get_firefox_link, "href"),
                        "/en-US/")
        sites.click_and_check(sites.get_firefox_link,"Welcome :: Firefox Input")
        sites.go_back()

        self.assertTrue(sites.is_element_visible(sites.get_themes_link))
        self.assertEqual(sites.get_atribute(sites.get_themes_link, "href"),
                         "/en-US/themes")
        sites.click_and_check(sites.get_themes_link,"Themes :: Firefox Input")
        sites.go_back()

        self.assertTrue(sites.is_element_visible(sites.get_feedback_link))
        self.assertEqual(sites.get_atribute(sites.get_feedback_link, "href"),
                         "/en-US/")
        sites.click_and_check(sites.get_feedback_link,"Welcome :: Firefox Input")
        sites.go_back(
                      )
        self.assertTrue(sites.is_element_visible(sites.get_sites_link))
        self.assertEqual(sites.get_atribute(sites.get_sites_link, "href"),
                         "/en-US/sites")
        sites.click_and_check(sites.get_sites_link,"Sites :: Firefox Input")


    @xfail(reason="Bug 650917 - Unable to select mobile product from Sites page")
    def test_product_and_type_filter(self):

        sites = sites_page.SitesPage(self.selenium)
        sites.go_to_sites_page()

        types = sites.type_filter.types()
        for t in types:
            t.select()
            self.assertTrue(t.is_selected)
            self.assertTrue(sites.contains_item(sites.get_type_list, t.name))

        self.assertEqual(len(sites.product_filter.products), len(self._products))

        for product in self._products:
            versions = list(product["versions"])
            sites.product_filter.select_product(product["name"])
            self.assertEqual(len(sites.product_filter.versions), len(versions))
        #TODO Platform filter

if __name__ == "__main__":
    unittest.main()

