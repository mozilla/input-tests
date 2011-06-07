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


import re

from unittestzero import Assert

import theme_page
import themes_page


class TestThemePage:

    _timestamp_regex = '\d+ \w+ \w+'

    def test_navigate_to_theme_page(self, testsetup):
        '''
        This testcase covers #15170 in Litmus
        Verify you are able to navigate to individual theme page, includes # of messages,
        page title = THEME, includes link 'Back to all themes', a relative date '1 day ago',
        the user platform, language 3. Verify timestamp link goes to the suggestion, the
        Platform link goes to that product filter, verify language goes to locale filter.
        '''
        themes_pg = themes_page.ThemesPage(testsetup)
        themes_pg.go_to_themes_page()
        themes_pg.themes[0].click_similar_messages()
        theme_pg = theme_page.ThemePage(testsetup)

        Assert.equal(theme_pg.messages_heading, "Theme")
        Assert.true(theme_pg.is_back_link_visible())
        Assert.true(theme_pg.is_message_count_visble())

    def test_platform_link_goes_to_product_filter(self, testsetup):
        themes_pg = themes_page.ThemesPage(testsetup)
        themes_pg.go_to_themes_page()
        themes_pg.themes[0].click_similar_messages()
        theme_pg = theme_page.ThemePage(testsetup)

        [Assert.true(message.is_platform_visble()) for message in theme_pg.messages]

        platform = theme_pg.message(1).platform
        theme_pg.message(1).click_platform_link()
        filter = theme_pg.platform_from_url
        Assert.true(theme_pg.message(1).platform_goes_to_product_filter(platform, filter))

    def test_language_link_goes_to_locale_filter(self, testsetup):
        themes_pg = themes_page.ThemesPage(testsetup)
        themes_pg.go_to_themes_page()
        themes_pg.themes[0].click_similar_messages()
        theme_pg = theme_page.ThemePage(testsetup)

        [Assert.true(message.is_language_visible()) for message in theme_pg.messages]

        language = theme_pg.message(1).locale
        theme_pg.message(1).click_locale_link()
        locale = theme_pg.locale_from_url
        Assert.true(theme_pg.message(1).language_goes_to_locale_filter(language, locale))

    def test_timestamp_link(self, testsetup):
        themes_pg = themes_page.ThemesPage(testsetup)
        themes_pg.go_to_themes_page()
        themes_pg.themes[0].click_similar_messages()
        theme_pg = theme_page.ThemePage(testsetup)

        relative_date = theme_pg.message(1).time
        matches = re.search(self._timestamp_regex, relative_date)
        Assert.true(int(matches.start()) > -1)
