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
#   Bebe <florin.strugariu@softvision.ro>
#   Dave Hunt <dhunt@mozilla.com>
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

from page import Page


class SitesFilterRegion(Page):

    _sites_filter_region_locator = "id('filter_sites')"

    @property
    def sites_filter_header(self):
        return self.selenium.get_text("xpath=%s/h3/a/text()[1]" % self._sites_filter_region_locator)

    @property
    def sites_filter_count(self):
        return int(self.selenium.get_xpath_count("%s//li" % self._sites_filter_locator))

    def sites_filter(self, lookup):
        return self.SitesFilter(self.testsetup, lookup)

    def contains_sites_filter(self, lookup):
        try:
            self.selenium.get_text("css=#filter_sites li:contains(%s) a > strong" % lookup)

            return True
        except:
            return False

    def sites_filters(self):
        return [self.SitesFilter(self.testsetup, i)for i in range(self.sites_filter_count)]

    class SitesFilter(Page):

        _name_locator = " a > strong"
        _site_count_locator = " .count"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self.root_locator + relative_locator

        @property
        def root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "css=#filter_sites li:nth(%s)" % self.lookup
            else:
                # lookup by name
                return "css=#filter_sites li:contains(%s)" % self.lookup

        @property
        def name(self):
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        @property
        def site_count(self):
            return self.selenium.get_text(self.absolute_locator(self._site_count_locator))

        def select(self):
            self.selenium.click(self.absolute_locator(self._name_locator))
            self.selenium.wait_for_page_to_load(self.timeout)
