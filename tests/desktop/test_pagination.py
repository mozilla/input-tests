#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage
from pages.desktop.themes import ThemesPage

xfail = pytest.mark.xfail


class TestPagination:

    @xfail(reason="Bug 716852 - No themes data on any environment, Bug 617177 - Filter type (happy/sad) doesn't persist when paginating through Themes")
    @pytest.mark.nondestructive
    def test_themes_filters_persist_when_paging_through_results(self, mozwebqa):
        """This testcase covers # 15018 in Litmus.

        1. Verifies the filter is in the URL
        2. Verifies the currently applied filter is styled appropriately
        3. Verifies the results of the filter

        """
        themes_pg = ThemesPage(mozwebqa)

        themes_pg.go_to_themes_page()
        themes_pg.type_filter.click_issues()
        themes_pg.click_older_messages()
        Assert.equal(themes_pg.feedback_type_from_url, "issue")
        Assert.equal(themes_pg.type_filter.selected_type, "Issues")
        [Assert.equal(theme.type, "Issue") for theme in themes_pg.themes]

    @pytest.mark.nondestructive
    def test_search_pagination(self, mozwebqa):
        """Litmus 13636 - Input: Verify Search results have pagination."""
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()
        feedback_pg.search_for("facebook")

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_visible)
        Assert.false(feedback_pg.is_newer_messages_link_enabled)

        Assert.equal(feedback_pg.older_messages_link, u"\xab Older Messages")
        Assert.equal(feedback_pg.newer_messages_link, u"Newer Messages \xbb")

        feedback_pg.click_older_messages()
        Assert.equal(feedback_pg.product_from_url, "firefox")
        Assert.equal(feedback_pg.search_term_from_url, "facebook")

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_visible)

        Assert.true(feedback_pg.is_older_messages_link_enabled)
        Assert.true(feedback_pg.is_newer_messages_link_enabled)

        Assert.equal(feedback_pg.older_messages_link, u"\xab Older Messages")
        Assert.equal(feedback_pg.newer_messages_link, u"Newer Messages \xbb")

        Assert.equal(feedback_pg.page_from_url, 2)

        feedback_pg.click_newer_messages()
        Assert.equal(feedback_pg.product_from_url, "firefox")
        Assert.equal(feedback_pg.search_term_from_url, "facebook")

        Assert.true(feedback_pg.is_older_messages_link_visible)
        Assert.true(feedback_pg.is_newer_messages_link_visible)

        Assert.true(feedback_pg.is_older_messages_link_enabled)
        Assert.false(feedback_pg.is_newer_messages_link_enabled)

        Assert.equal(feedback_pg.older_messages_link, u"\xab Older Messages")
        Assert.equal(feedback_pg.newer_messages_link, u"Newer Messages \xbb")

        Assert.equal(feedback_pg.page_from_url, 1)
