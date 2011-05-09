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
# Contributor(s): teodosia.pop@softvision.ro
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
Created on Apr 21, 2011
'''

from selenium import selenium
from vars import ConnectionParameters
import unittest

import theme_page
import themes_page


class TestThemePage(unittest.TestCase):
    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()
        
    def test_navigate_to_theme_page(self):
        '''
        This testcase covers #15170 in Litmus
        Verify you are able to navigate to individual theme page, 
        includes # of messages, page title = THEME, includes link 
        'Back to all themes', each theme is listed with a lightbulb icon, 
        the suggestion text, a relative date '1 day ago', the user platform, 
        language 3. Verify timestamp link goes to the suggestion, 
        the Platform link goes to that product filter, verify language
        goes to locale filter.
        '''
        themes_pg = themes_page.ThemesPage(self.selenium)
        
        themes_pg.go_to_themes_page()
        #navigate to individual theme page
        theme_msg = themes_pg.themes
        theme_msg[0].click_similar_messages()
        theme = theme_page.ThemePage(self.selenium)
        
        #page title = THEME
        self.assertEqual(theme.messages_heading, "Theme")
        
        #includes link 'Back to all themes'
        self.assertTrue(theme.is_back_to_all_themes_link_visible())
                
        #message number
        self.assertTrue(theme.is_message_count_visble())
                
    def test_platform_link(self):
        themes_pg = themes_page.ThemesPage(self.selenium)
        themes_pg.go_to_themes_page()
        theme_msg = themes_pg.themes
        theme_msg[0].click_similar_messages()
        theme = theme_page.ThemePage(self.selenium)
        
        #includes the user platform
        self.assertTrue(theme.message(1).is_platform_visble())
        
        #Platform link goes to that product filter
        theme.click_platform_link()
        filter = theme.platform_from_url
        platform = theme.message(1).platform
        self.assertTrue(theme.platform_goes_to_product_filter(filter, platform))
        
    def test_locale_link(self):
        themes_pg = themes_page.ThemesPage(self.selenium)
        themes_pg.go_to_themes_page()
        theme_msg = themes_pg.themes
        theme_msg[0].click_similar_messages()
        theme = theme_page.ThemePage(self.selenium)
        
        #check if language visible
        self.assertTrue(theme.message(1).is_language_visible())
    
        #verify language goes to locale filter
        theme.click_locale_link()
        language = theme.message(1).locale
        locale = theme.locale_from_url
        self.assertTrue(theme.language_goes_to_locale_filter(language, locale))
        
    def test_timestamp_link(self):
        themes_pg = themes_page.ThemesPage(self.selenium)
        themes_pg.go_to_themes_page()
        theme_msg = themes_pg.themes
        theme_msg[0].click_similar_messages()
        theme = theme_page.ThemePage(self.selenium)
        
        #relative date '1 day ago'
        relative_date = theme.message(1).time
        self.assertTrue(relative_date.endswith(" ago"))
        
if __name__ == "__main__":
    unittest.main()