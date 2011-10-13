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


class Header(Page):

    _feedback_link_locator = "css=a.dashboard"
    _themes_link_locator = "css=a.themes"
    _main_heading_link_locator = "css=h1 > a"
    _sites_link_locator = "css=a.issues"

    def click_feedback_link(self):
        self.is_feedback_link_visible
        self.selenium.click(self._feedback_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

        from pages.desktop.feedback import FeedbackPage
        return FeedbackPage(self.testsetup)

    def click_themes_link(self):
        self.is_themes_link_visible
        self.selenium.click(self._themes_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

        from pages.desktop.themes import ThemesPage
        return ThemesPage(self.testsetup)

    def click_main_heading_link(self):
        self.is_main_heading_link_visible
        self.selenium.click(self._main_heading_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

        from pages.desktop.feedback import FeedbackPage
        return FeedbackPage(self.testsetup)

    def click_sites_link(self):
        self.is_sites_link_visible
        self.selenium.click(self._sites_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

        from pages.desktop.sites import SitesPage
        return SitesPage(self.testsetup)

    @property
    def is_feedback_link_visible(self):
        return self.selenium.is_visible(self._feedback_link_locator)

    @property
    def is_themes_link_visible(self):
        return self.selenium.is_visible(self._themes_link_locator)

    @property
    def is_main_heading_link_visible(self):
        return self.selenium.is_visible(self._main_heading_link_locator)

    @property
    def is_sites_link_visible(self):
        return self.selenium.is_visible(self._sites_link_locator)
