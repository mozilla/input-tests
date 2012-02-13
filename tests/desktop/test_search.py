#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage


class TestSearch:

    @pytest.mark.nondestructive
    def test_that_empty_search_of_feedback_returns_some_data(self, mozwebqa):
        """Litmus 13847"""
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        feedback_pg.search_for('')
        Assert.greater(len(feedback_pg.messages), 0)

    @pytest.mark.nondestructive
    def test_that_we_can_search_feedback_with_unicode(self, mozwebqa):
        """Litmus 13697"""
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        # Select the Firefox version that is 1 less than the newest to ensure the unicode
        # search returns at least 1 result.
        feedback_pg.product_filter.select_product('firefox')
        feedback_pg.product_filter.select_version('--')

        feedback_pg.search_for(u"rapidit\xe9")
        Assert.greater(len(feedback_pg.messages), 0)

    @pytest.mark.nondestructive
    def test_search_box_placeholder(self, mozwebqa):
        """Litmus 13845.

        1. Verify that there is a search field appearing in Latest Feedback
        section it shows by default "Search by keyword"

        """
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.search_box_placeholder, "Search by keyword")
