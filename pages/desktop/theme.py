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
#                 Matt Brandt <mbrandt@mozilla.com>
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
Created on March 28, 2010
'''
from pages.base import InputBasePage
from pages.desktop.regions.message import Message


class ThemePage(InputBasePage):

    _messages_heading_locator = "css=#messages h2"
    _theme_callout_locator = "id=theme-callout"
    _back_link_locator = "css=a.exit"
    _messages_locator = "id('messages')//li[@class='message']"
    _relative_date = "css=.meta a"
    _total_message_count_locator = "css=#big-count p" 

    def is_back_link_visible(self):
        """
        Returns true if the "Back to all themes" link is visible
        """
        return self.selenium.is_visible(self._back_link_locator)

    def is_message_count_visible(self):
        """
        Returns True if the message count is visible
        """
        return self.selenium.is_visible(self._total_message_count_locator)

    @property
    def messages_heading(self):
        """
        Returns the heading text of the Theme page
        """
        return self.selenium.get_text(self._messages_heading_locator)

    @property
    def locale_filter(self):
        from pages.desktop.regions.locale_filter import LocaleFilter
        return LocaleFilter(self.testsetup)

    @property
    def platform_filter(self):
        from pages.desktop.regions.platform_filter import PlatformFilter
        return PlatformFilter.CheckboxFilter(self.testsetup)

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
    def message_count(self):
        return int(self.selenium.get_xpath_count(self._messages_locator))

    @property
    def messages(self):
        return [Message(self.testsetup, i + 1) for i in range(self.message_count)]

    def message(self, index):
        return Message(self.testsetup, index)
