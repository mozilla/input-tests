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
#   Teodosia Pop <teodosia.pop@softvision.ro>
#   Matt Brandt <mbrandt@mozilla.com>
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

import re

from unittestzero import Assert

from pages.desktop.themes import ThemesPage


class TestThemePage:

    def test_navigate_to_theme_page(self, mozwebqa):
        """This testcase covers #15170 in Litmus.

        Verify you are able to navigate to individual theme page, includes # of messages,
        page title = THEME, includes link 'Back to all themes', a relative date '1 day ago',
        the user platform, language 3. Verify timestamp link goes to the suggestion, the
        Platform link goes to that product filter, verify language goes to locale filter.

        """
        themes_pg = ThemesPage(mozwebqa)
        themes_pg.go_to_themes_page()
        theme_pg = themes_pg.themes[0].click_similar_messages()

        Assert.equal(theme_pg.messages_heading, "THEME")
        Assert.true(theme_pg.is_back_link_visible)
        Assert.true(theme_pg.is_message_count_visible)

    def test_platform_link_applies_platform_filter(self, mozwebqa):
        themes_pg = ThemesPage(mozwebqa)
        themes_pg.go_to_themes_page()
        theme_pg = themes_pg.themes[0].click_similar_messages()

        [Assert.true(message.is_platform_visible) for message in theme_pg.messages]

        platform = theme_pg.messages[0].platform
        theme_pg.messages[0].click_platform()

        Assert.true(theme_pg.platform_filter.platform(platform).is_selected)
        for message in theme_pg.messages:
            Assert.equal(message.platform, platform)

    def test_locale_link_applies_locale_filter(self, mozwebqa):
        themes_pg = ThemesPage(mozwebqa)
        themes_pg.go_to_themes_page()
        theme_pg = themes_pg.themes[0].click_similar_messages()

        [Assert.true(message.is_locale_visible) for message in theme_pg.messages]

        locale = theme_pg.messages[0].locale
        theme_pg.messages[0].click_locale()

        Assert.true(theme_pg.locale_filter.locale(locale).is_selected)
        for message in theme_pg.messages:
            Assert.equal(message.locale, locale)

    def test_value_of_timestamp_link(self, mozwebqa):
        themes_pg = ThemesPage(mozwebqa)
        themes_pg.go_to_themes_page()
        theme_pg = themes_pg.themes[0].click_similar_messages()

        for message in theme_pg.messages:
            Assert.not_none(re.match('(\d+ \w+ ago)|(\w{3} \d{1,2}, \d{4})', message.time))
