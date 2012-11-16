#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage

xfail = pytest.mark.xfail


class TestPagination:

    @pytest.mark.nondestructive
    def test_search_pagination(self, mozwebqa):
        """Litmus 13636 - Input: Verify Search results have pagination."""
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_version("--")
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
