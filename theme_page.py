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
Created on March 28, 2010
'''
import input_base_page
import message_region
from vars import ConnectionParameters

page_load_timeout = ConnectionParameters.page_load_timeout

class ThemePage(input_base_page.InputBasePage):

    _messages_heading_locator = "css=#messages h2"
    _theme_callout_locator = "id=theme-callout"
    _back_link_locator = "css=a.exit"
    _messages_locator = "id('messages')//li[@class='message']"
    _platform_link_locator = "//div[@id='messages']/ul/li/ul/li[2]/a"
    _locale_link_locator = "//div[@id='messages']/ul/li/ul/li[3]/a"
    _time_link_locator = "//div[@id='messages']/ul/li/ul/li[1]/a/time"
    _relative_date = "css=.meta a"

    def click_platform_link(self):
        self.selenium.click(self._platform_link_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)
        
    def click_locale_link(self):
        self.selenium.click(self._locale_link_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)
    
    def click_timestamp_link(self):
        self.selenium.click(self._time_link_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)
    
    def platform_goes_to_product_filter(self, filter, platform):
        platforms = {"Windows 7" : 1, 
                     "Windows XP": 2,
                     "Windows Vista" : 3,
                     "Linux" : 4,
                     "Mac OS X": 5,
                     "Android": 6,
                     "Maemo" : 7}
        filters = {"win7" : 1, 
                   "winxp": 2,
                   "vista" : 3,
                   "linux" : 4,
                   "mac": 5,
                   "android": 6,
                   "maemo" : 7}
        return platforms[platform] == filters[filter]
    
    def language_goes_to_locale_filter(self, language, locale):
        languages = {"English (US)": 1,
                     "Spanish": 2,
                     "English (British)": 3,
                     "Portuguese (Brazilian)": 4,
                     "German": 5,
                     "French": 6,
                     "Russian": 7,
                     "Italian": 8,
                     "Polish:": 9,
                     "Turkish": 10,
                     "Hungarian": 11}
        locales = {"en-US": 1,
                   "es": 2,
                   "en-GB": 3,
                   "pt-BR": 4,
                   "de": 5,
                   "fr": 6,
                   "ru": 7,
                   "it": 8,
                   "pl": 9,
                   "tr": 10,
                   "hu": 11}
        return languages[language] == locales[locale]
                                  
    @property
    def messages_heading(self):
        """
        Returns the heading text of the Theme page
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
    
    def is_back_to_all_themes_link_visible(self):
        """
        Returns true if the "Back to all themes" link is visible
        """
        return self.selenium.is_text_present("Back to all themes")
    
    def is_message_count_visble(self):
        """
        Returns True if the message count is visible
        """
        return self.selenium.is_text_present(self.message_count)
        
    @property
    def message_count(self):
        return int(self.selenium.get_xpath_count(self._messages_locator))

    @property
    def messages(self):
        return [message_region.Message(self.selenium, i + 1) for i in range(self.message_count)]

    def message(self, index):
        return message_region.Message(self.selenium, index)
    
    @property
    def time_link(self):
        return self.selenium.get_text(self._time_link_locator)
