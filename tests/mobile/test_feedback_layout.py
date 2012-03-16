#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.mobile.feedback import FeedbackPage

xfail = pytest.mark.xfail


class Test_Feedback_Layout:

    @xfail(reason="Bug 715542 - visiting the mobile site returns a 500 error")
    @pytest.mark.nondestructive
    def test_the_header_layout(self, mozwebqa):

        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()

        Assert.true(feedback_pg.is_feed_visible)
        Assert.false(feedback_pg.is_statistics_visible)
        Assert.false(feedback_pg.is_settings_visible)

        feedback_pg.click_settings_tab()

        Assert.false(feedback_pg.is_feed_visible)
        Assert.false(feedback_pg.is_statistics_visible)
        Assert.true(feedback_pg.is_settings_visible)

        feedback_pg.click_statistics_tab()

        Assert.false(feedback_pg.is_feed_visible)
        Assert.true(feedback_pg.is_statistics_visible)
        Assert.false(feedback_pg.is_settings_visible)

        feedback_pg.click_feed_tab()

        Assert.true(feedback_pg.is_feed_visible)
        Assert.false(feedback_pg.is_statistics_visible)
        Assert.false(feedback_pg.is_settings_visible)

    @pytest.mark.nondestructive
    def test_that_checks_pagination(self, mozwebqa):
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()

        Assert.false(feedback_pg.is_older_feedback_button_disabled)
        Assert.true(feedback_pg.is_newer_feedback_button_disabled)

        feedback_pg.click_older_feedback_button()
        Assert.false(feedback_pg.is_newer_feedback_button_disabled)

        # return to first page
        feedback_pg.click_newer_feedback_button()
        Assert.false(feedback_pg.is_older_feedback_button_disabled)
        Assert.true(feedback_pg.is_newer_feedback_button_disabled)
