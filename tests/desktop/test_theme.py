#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from unittestzero import Assert
import pytest

from pages.desktop.themes import ThemesPage


class TestThemePage:

    @pytest.mark.xfail(reason='Bug 716852 - No themes data on any environment')
    @pytest.mark.nondestructive
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

    @pytest.mark.xfail(reason='Bug 716852 - No themes data on any environment')
    @pytest.mark.nondestructive
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

    @pytest.mark.xfail(reason='Bug 716852 - No themes data on any environment')
    @pytest.mark.nondestructive
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

    @pytest.mark.xfail(reason='Bug 716852 - No themes data on any environment')
    @pytest.mark.nondestructive
    def test_value_of_timestamp_link(self, mozwebqa):
        themes_pg = ThemesPage(mozwebqa)
        themes_pg.go_to_themes_page()
        theme_pg = themes_pg.themes[0].click_similar_messages()

        for message in theme_pg.messages:
            Assert.not_none(re.match('(\d+ \w+ ago)|(\w{3} \d{1,2}, \d{4})', message.time))
