#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.mobile.feedback import FeedbackPage


class TestSearch:

    pozitive_search_term = "firefox"

    @pytest.mark.nondestructive
    def test_that_search_returns_results(self, mozwebqa):
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()

        feedback_pg.search_for(self.pozitive_search_term)
        messages = feedback_pg.messages

        Assert.equal(self.pozitive_search_term, feedback_pg.search_term_from_url)
        Assert.greater(len(messages), 0)

    @pytest.mark.nondestructive
    def test_that_empty_search_of_feedback_returns_some_data(self, mozwebqa):
        """Litmus 13847"""
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        feedback_pg.search_for('')
        Assert.greater(len(feedback_pg.messages), 0)

    @pytest.mark.nondestructive
    def test_search_box_placeholder(self, mozwebqa):
        """Litmus 13845"""
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.search_box_placeholder, "Search by keyword")

    @pytest.mark.nondestructive
    def test_that_search_results_contain_search_text(self, mozwebqa):
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()

        feedback_pg.search_for(self.pozitive_search_term)

        for message in feedback_pg.messages:
            Assert.contains(self.pozitive_search_term, message.body.lower())
