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
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#                 Alex Lakatos <alex.lakatos@softvision.ro>
#                 Matt Brandt <mbrandt@mozilla.com>
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

Created on Nov 30, 2010

'''

from datetime import date
from datetime import timedelta
import random
import string

from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail

import feedback_page


class TestSearchDates:

    xfail(reason="Bug 678219 - [stage] Date format in the GET request changed from '2011-08-10' to '08%2F10%2F2011'")
    def test_feedback_preset_date_filters(self, mozwebqa):
        """

        This testcase covers # 13605 & 13606 in Litmus
        1. Verifies the preset date filters of 1, 7, and 30 days

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.date_filter.current_days, u"\u221e")

        day_filters = ((1, "1d", "Last day"), (7, "7d", "Last 7 days"), (30, "30d", "Last 30 days"))
        for days in day_filters:
            Assert.equal(feedback_pg.date_filter.get_days_tooltip(days[1]), days[2])
            feedback_pg.date_filter.click_days(days[1])
            Assert.equal(feedback_pg.date_filter.current_days, days[1])
            start_date = date.today() - timedelta(days=days[0])
            Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%Y-%m-%d'))
            # TODO: Check results are within the expected date range, possibly by navigating to the last page and checking the final result is within range. Currently blocked by bug 615844.

    def test_feedback_custom_date_filter(self, mozwebqa):
        """

        This testcase covers # 13605, 13606 & 13715 in Litmus
        1. Verifies the calendar is displayed when filtering on custom dates
        2. Verifies date-start=<date> and end-date=<date> in the url

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.date_filter.custom_dates_tooltip, "Custom")

        start_date = date.today() - timedelta(days=3)
        end_date = date.today() - timedelta(days=1)

        feedback_pg.date_filter.filter_by_custom_dates_using_datepicker(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%Y-%m-%d'))
        Assert.equal(feedback_pg.date_end_from_url, end_date.strftime('%Y-%m-%d'))
        # TODO: Check results are within the expected date range, possibly by navigating to the first/last pages and checking the final result is within range. Currently blocked by bug 615844.

        # Check that the relevant days preset link is highlighted when the applied custom date filter matches it
        day_filters = ((1, "1d"), (7, "7d"), (30, "30d"))
        for days in day_filters:
            start_date = date.today() - timedelta(days=days[0])
            feedback_pg.date_filter.filter_by_custom_dates_using_datepicker(start_date, date.today())
            Assert.false(feedback_pg.date_filter.is_custom_date_filter_visible)
            Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%Y-%m-%d'))
            Assert.equal(feedback_pg.date_end_from_url, date.today().strftime('%Y-%m-%d'))
            Assert.equal(feedback_pg.date_filter.current_days, days[1])

    def test_feedback_custom_date_filter_with_random_alphabet(self, mozwebqa):
        """

        This testcase covers # 13607 in Litmus
        1.Verifies custom date fields do not accept alphabet

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        letters = 'abcdefghijklmnopqrstuvwxyz'
        start_date = ''.join(random.sample(letters, 8))
        end_date = ''.join(random.sample(letters, 8))

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, '')
        Assert.equal(feedback_pg.date_end_from_url, '')

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, '')
        Assert.equal(feedback_pg.date_filter.custom_end_date, '')

    def test_feedback_custom_date_filter_with_random_numbers(self, mozwebqa):
        """

        This testcase covers # 13608 in Litmus
        1.Verifies random numbers show all recent feedback

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = random.randint(10000000, 50000000)
        end_date = random.randint(50000001, 99999999)

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, str(start_date))
        Assert.equal(feedback_pg.date_end_from_url, str(end_date))

        Assert.equal(feedback_pg.message_count, 20)

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, str(start_date))
        Assert.equal(feedback_pg.date_filter.custom_end_date, str(end_date))

    def test_feedback_custom_date_filter_with_invalid_dates(self, mozwebqa):
        """

        This testcase covers # 13609 , 13725 in Litmus
        1.Verifies invalid dates show all recent feedback

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = "0000-00-00"
        end_date = "0000-00-00"

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date)
        Assert.equal(feedback_pg.date_end_from_url, end_date)

        Assert.equal(feedback_pg.message_count, 20)

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, start_date)
        Assert.equal(feedback_pg.date_filter.custom_end_date, end_date)

    def test_feedback_custom_date_filter_with_future_dates(self, mozwebqa):
        """

        This testcase covers # 13612 in Litmus
        1.Verifies future dates generate an error

        """

        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = "2021-01-01"
        end_date = "2031-01-01"

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date)
        Assert.equal(feedback_pg.date_end_from_url, end_date)

        Assert.equal(feedback_pg.warning_heading, 'No search results found.')

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, start_date)
        Assert.equal(feedback_pg.date_filter.custom_end_date, end_date)

    def test_feedback_custom_date_filter_with_future_start_date(self, mozwebqa):
        """

        This testcase covers # 13610 in Litmus
        1.Verifies future start date are ignored as erroneous input and results for a 30 day period are returned

        """

        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = "2900-01-01"
        end_date = ""

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date)
        Assert.equal(feedback_pg.date_end_from_url, end_date)

        Assert.equal(feedback_pg.message_count, 20)

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, start_date)
        Assert.equal(feedback_pg.date_filter.custom_end_date, end_date)
    xfail(reason="Bug 686850 - Returned message counts vary too much to reliably test")
    def test_feedback_custom_date_filter_with_future_end_date(self, mozwebqa):
        """

        This testcase covers # 13611 in Litmus
        1. Verifies future end date filter data until current day

        """

        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = ""
        end_date = "2900-01-01"

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date)
        Assert.equal(feedback_pg.date_end_from_url, end_date)

        Assert.contains('Search Results', feedback_pg.message_column_heading)

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, start_date)
        Assert.equal(feedback_pg.date_filter.custom_end_date, end_date)

    def test_feedback_custom_date_filter_with_end_date_lower_than_start_date(self, mozwebqa):
        """

        This testcase covers # 13613, 13724 in Litmus
        1. Verifies start_date > end_date get switched automatically and the results are shown from end date to start date

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = date.today() - timedelta(days=1)
        end_date = date.today() - timedelta(days=3)

        feedback_pg.date_filter.filter_by_custom_dates_using_datepicker(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%Y-%m-%d'))
        Assert.equal(feedback_pg.date_end_from_url, end_date.strftime('%Y-%m-%d'))
        # TODO: Check results are within the expected date range, possibly by navigating to the first/last pages and checking the final result is within range. Currently blocked by bug 615844.

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, start_date.strftime('%Y-%m-%d'))
        Assert.equal(feedback_pg.date_filter.custom_end_date, end_date.strftime('%Y-%m-%d'))

    def test_feedback_custom_date_filter_with_mdy_format(self, mozwebqa):
        """

        This testcase covers # 13614 in Litmus
        1.Verifies custom date fields show all recent feedback

        """
        feedback_pg = feedback_page.FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()

        start_date = '04-22-2011'
        end_date = ''

        feedback_pg.date_filter.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, start_date)
        Assert.equal(feedback_pg.date_end_from_url, '')

        Assert.equal(feedback_pg.message_count, 20)

        feedback_pg.date_filter.click_custom_dates()
        Assert.equal(feedback_pg.date_filter.custom_start_date, start_date)
        Assert.equal(feedback_pg.date_filter.custom_end_date, '')
