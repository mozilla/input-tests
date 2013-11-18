#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage


class TestLocaleFilter:

    @pytest.mark.nondestructive
    def test_feedback_can_be_filtered_by_locale(self, mozwebqa):
        """This testcase covers # 15120 in Litmus.

        1. Verify that the number of messages in the locale list matches the number of messages returned
        2. Verify that the locale short code appears in the URL
        3. Verify that the locale for all messages on the first page of results is correct

        """
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product('firefox')

        locale_name = "Russian"
        locale = feedback_pg.locale_filter.locale(locale_name)
        locale_message_count = locale.message_count
        locale_code = locale.code
        locale.select()

        Assert.equal(feedback_pg.total_message_count, locale_message_count)
        Assert.equal(feedback_pg.locale_from_url, locale_code)
        [Assert.equal(message.locale, locale_name) for message in feedback_pg.messages]

    @pytest.mark.xfail(reason='Bug 940361 - response counts for a locale in sidebar change when you select the locale')
    @pytest.mark.skipif("not config.getvalue('base_url').endswith('allizom.org')")
    @pytest.mark.nondestructive
    def test_feedback_can_be_filtered_by_locale_from_expanded_list(self, mozwebqa):
        """This testcase covers # 15087 & 15120 in Litmus.

        1. Verify the initial locale count is 10
        2. Verify clicking the more locales link shows additional locales
        3. Verify filtering by one of the additional locales
        4. Verify that the number of messages in the locale list matches the number of messages returned
        5. Verify that the locale short code appears in the URL
        6. Verify that the locale for all messages on the first page of results is correct

        """
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product('firefox')

        Assert.equal(len(feedback_pg.locale_filter.locales), 10)

        locale_names = []
        for locale in feedback_pg.locale_filter.locales:
            locale_names.append(locale.name)
        for locale_name in locale_names:
            locale = feedback_pg.locale_filter.locale(locale_name)
            locale_message_count = locale.message_count
            locale_code = locale.code
            locale.select()
            Assert.equal(feedback_pg.total_message_count, locale_message_count)
            Assert.equal(feedback_pg.locale_from_url, locale_code)
            [Assert.equal(message.locale, locale_name) for message in feedback_pg.messages]

            # Un-select selected locale
            locale = feedback_pg.locale_filter.locale(locale_name)
            locale.select()
