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

page_load_timeout = ConnectionParameters.page_load_timeout


class SitesPage(input_base_page.InputBasePage):

    _page_title = 'Sites :: Firefox Input'
    _first_similar_messages_link_locator = "//ul[@class='themes']/li[@class='theme'][1]/p[@class='primary']/a"
    _messages_heading_locator = "css=#messages h2"
    _theme_callout_locator = "id=theme-callout"
    _back_link_locator = "css=a.exit"
    _first_message_url_link_locator = "//li[@class='message'][1]/ul[@class='meta']/li[4]/a"

    def __init__(self, selenium):
        self.selenium = selenium

    def go_to_sites_page(self):
        self.selenium.open('/sites/')
        self.is_the_current_page

    def click_site(self, lookup, by="index"):
        if by == "url":
            self.selenium.click("link=" + lookup)
        elif by == "index":
            self.selenium.click("//li[@class='site'][" + lookup + "]/p[@class='name']/a")

        self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_first_similar_messages_link(self):
        self.selenium.click(self._first_similar_messages_link_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    @property
    def messages_heading(self):
        """

        Returns the heading text of the Themes page

        """
        return self.selenium.get_text(self._messages_heading_locator)

    @property
    def theme_callout(self):
        """

        Returns the text value of the theme callout

        """
        return self.selenium.get_text(self._theme_callout_locator)

    @property
    def back_link(self):
        """

        Returns the text value of the back link

        """
        return self.selenium.get_text(self._back_link_locator)

    @property
    def first_message_url(self):
        """

        Returns the text value of the first message's URL link

        """
        return self.selenium.get_text(self._first_message_url_link_locator)

    def site_url(self, index):
        """

        Returns the name of the currently selected site

        """
        return self.selenium.get_text("//li[@class='site'][" + str(index) + "]/p[@class='name']/a");
