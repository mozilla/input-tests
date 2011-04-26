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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
#                 David Burns
#                 Dave Hunt <dhunt@mozilla.com>
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
Created on Nov 24, 2010
'''
import input_base_page
from vars import ConnectionParameters

import product_filter_region
import type_filter_region

page_load_timeout = ConnectionParameters.page_load_timeout


class SitesPage(input_base_page.InputBasePage):

    _page_title = 'Sites :: Firefox Input'

    _sites_locator = "id('themes')//li[@class='site']"

    _feedback_link_locator = "css=a.dashboard"
    _themes_link_locator = "css=a.themes"
    _firefox_link_locator = "link=Firefox Input Dashboard"
    _sites_link_locator = "css=a.issues"

    _type_list = ("All",
                  "Praise",
                  "Issues",
                  "Ideas")
    def go_to_sites_page(self):
        self.selenium.open('/sites/')
        self.is_the_current_page

    @property
    def get_type_list(self):
        return self._type_list

    @property
    def get_feedback_link(self):
        return self._feedback_link_locator

    @property
    def get_themes_link(self):
        return self._themes_link_locator

    @property
    def get_firefox_link(self):
        return self._firefox_link_locator

    @property
    def get_sites_link(self):
        return self._sites_link_locator

    @property
    def product_filter(self):
        return product_filter_region.ProductFilter.ComboFilter(self.selenium)

    @property
    def type_filter(self):
        return type_filter_region.TypeFilter.ButtonFilter(self.selenium)

    @property
    def site_count(self):
        return int(self.selenium.get_xpath_count(self._sites_locator))

    @property
    def sites(self):
        return [self.Site(self.selenium, i + 1) for i in range(self.site_count)]

    def site(self, index):
        return self.Site(self.selenium, index)

    class Site(object):

        _name_locator = " .name a"
        _ssh_locator = " .name span"

        def __init__(self, selenium, index):
            self.selenium = selenium
            self.index = index

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            return "css=#themes .site:nth(%s)" % (self.index - 1)

        def href_atribute_locator(self, _locator):
            return _locator + "@href"

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        def click_name(self):
            self.selenium.click(self.absolute_locator(self._name_locator))
            self.selenium.wait_for_page_to_load(page_load_timeout)

        @property
        def url(self):
            return self.selenium.get_attribute(self.href_atribute_locator(self.absolute_locator(self._name_locator)))

        @property
        def is_ssh(self):
            if "https" in self.url:
                try:
                    self.selenium.get_text(self.absolute_locator(self._ssh_locator))
                    return True
                except:
                    return False
            else:
                return False