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

    def test_feedback_preset_date_filters(self, testsetup):
        """

        This testcase covers # 13605 & 13606 in Litmus
        1. Verifies the preset date filters of 1, 7, and 30 days

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.get_current_days(), None)

        day_filters = ((1, "1d", "Last day"), (7, "7d", "Last 7 days"), (30, "30d", "Last 30 days"))
        for days in day_filters:
            Assert.equal(feedback_pg.get_days_tooltip(days[1]), days[2])
            feedback_pg.click_days(days[1])
            Assert.equal(feedback_pg.get_current_days(), days[1])
            start_date = date.today() - timedelta(days=days[0])
            # The format for a date when using preset filters is different to using the custom search. See bug 616306 for details.
            Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%Y-%m-%d'))
            # TODO: Check results are within the expected date range, possibly by navigating to the last page and checking the final result is within range. Currently blocked by bug 615844.

    def test_feedback_custom_date_filter(self, testsetup):
        """

        This testcase covers # 13605, 13606 & 13715 in Litmus
        1. Verifies the calendar is displayed when filtering on custom dates
        2. Verifies date-start=<date> and end-date=<date> in the url

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.get_custom_dates_tooltip(), "Custom")

        start_date = date.today() - timedelta(days=3)
        end_date = date.today() - timedelta(days=1)

        feedback_pg.filter_by_custom_dates_using_datepicker(start_date, end_date)
        # The format for a date when using preset filters is different to using the custom search. See bug 616306 for details.
        Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%m%%2F%d%%2F%Y'))
        Assert.equal(feedback_pg.date_end_from_url, end_date.strftime('%m%%2F%d%%2F%Y'))
        # TODO: Check results are within the expected date range, possibly by navigating to the first/last pages and checking the final result is within range. Currently blocked by bug 615844.

        # Check that the relevant days preset link is highlighted when the applied custom date filter matches it
        day_filters = ((1, "1d"), (7, "7d"), (30, "30d"))
        for days in day_filters:
            start_date = date.today() - timedelta(days=days[0])
            feedback_pg.filter_by_custom_dates_using_datepicker(start_date, date.today())
            Assert.false(feedback_pg.is_custom_date_filter_visible())
            # The format for a date when using preset filters is different to using the custom search. See bug 616306 for details.
            Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%m%%2F%d%%2F%Y'))
            Assert.equal(feedback_pg.date_end_from_url, date.today().strftime('%m%%2F%d%%2F%Y'))
            Assert.equal(feedback_pg.get_current_days(), days[1])

    def test_feedback_custom_date_filter_with_random_alphabet(self, testsetup):
        """

        This testcase covers # 13607 in Litmus
        1.Verifies custom date fields do not accept alphabet

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        letters = 'abcdefghijklmnopqrstuvwxyz'
        start_date = ''.join(random.sample(letters, 8))
        end_date = ''.join(random.sample(letters, 8))

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, '')
        Assert.equal(feedback_pg.date_end_from_url, '')

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, '')
        Assert.equal(feedback_pg.custom_end_date, '')

    def test_feedback_custom_date_filter_with_random_numbers(self, testsetup):
        """

        This testcase covers # 13608 in Litmus
        1.Verifies random numbers generate an error

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = random.randint(10000000, 50000000)
        end_date = random.randint(50000001, 99999999)

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, str(start_date))
        Assert.equal(feedback_pg.date_end_from_url, str(end_date))

        Assert.equal(feedback_pg.warning, 'No search results found.')

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, str(start_date))
        Assert.equal(feedback_pg.custom_end_date, str(end_date))
        Assert.equal(feedback_pg.custom_date_first_error, 'Enter a valid date.')
        Assert.equal(feedback_pg.custom_date_second_error, 'Enter a valid date.')

    def test_feedback_custom_date_filter_with_invalid_dates(self, testsetup):
        """

        This testcase covers # 13609 , 13725 in Litmus
        1.Verifies invalid dates generate an error

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = "00/00/0000"
        end_date = "00/00/0000"

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, string.replace(start_date, '/', '%2F'))
        Assert.equal(feedback_pg.date_end_from_url, string.replace(end_date, '/', '%2F'))

        Assert.equal(feedback_pg.warning, 'No search results found.')

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, start_date)
        Assert.equal(feedback_pg.custom_end_date, end_date)
        Assert.equal(feedback_pg.custom_date_first_error, 'Enter a valid date.')
        Assert.equal(feedback_pg.custom_date_second_error, 'Enter a valid date.')

    def test_feedback_custom_date_filter_with_future_dates(self, testsetup):
        """

        This testcase covers # 13612 in Litmus
        1.Verifies future dates generate an error

        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = "01/01/2021"
        end_date = "01/01/2031"

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, string.replace(start_date, '/', '%2F'))
        Assert.equal(feedback_pg.date_end_from_url, string.replace(end_date, '/', '%2F'))

        Assert.equal(feedback_pg.warning, 'No search results found.')

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, start_date)
        Assert.equal(feedback_pg.custom_end_date, end_date)

    @xfail(reason="Bug 645850 - [input-stage] Internal Server Error - OverflowError: mktime argument out of range")
    def test_feedback_custom_date_filter_with_future_start_date(self, testsetup):
        """

        This testcase covers # 13610 in Litmus
        1.Verifies future start date generate an error

        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = "01/01/2900"
        end_date = ""

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, string.replace(start_date, '/', '%2F'))
        Assert.equal(feedback_pg.date_end_from_url, string.replace(end_date, '/', '%2F'))

        Assert.equal(feedback_pg.warning, 'No search results found.')

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, start_date)
        Assert.equal(feedback_pg.custom_end_date, end_date)

    @xfail(reason="Bug 645850 - [input-stage] Internal Server Error - OverflowError: mktime argument out of range")
    def test_feedback_custom_date_filter_with_future_end_date(self, testsetup):
        """

        This testcase covers # 13611 in Litmus
        1.Verifies future end date filter data untill current day

        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = ""
        end_date = "01/01/2900"

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, string.replace(start_date, '/', '%2F'))
        Assert.equal(feedback_pg.date_end_from_url, string.replace(end_date, '/', '%2F'))

        Assert.true(feedback_pg.is_text_present('Search Results'))

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, start_date)
        Assert.equal(feedback_pg.custom_end_date, end_date)

    def test_feedback_custom_date_filter_with_end_date_lower_than_start_date(self, testsetup):
        """

        This testcase covers # 13613, 13724 in Litmus
        1. Verifies start_date > end_date get switched automatically and the results are shown from end date to start date

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = date.today() - timedelta(days=1)
        end_date = date.today() - timedelta(days=3)

        feedback_pg.filter_by_custom_dates_using_datepicker(start_date, end_date)
        # The format for a date when using preset filters is different to using the custom search. See bug 616306 for details.
        Assert.equal(feedback_pg.date_start_from_url, start_date.strftime('%m%%2F%d%%2F%Y'))
        Assert.equal(feedback_pg.date_end_from_url, end_date.strftime('%m%%2F%d%%2F%Y'))
        # TODO: Check results are within the expected date range, possibly by navigating to the first/last pages and checking the final result is within range. Currently blocked by bug 615844.

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, start_date.strftime('%m/%d/%Y'))
        Assert.equal(feedback_pg.custom_end_date, end_date.strftime('%m/%d/%Y'))

    def test_feedback_custom_date_filter_with_ydm_format(self, testsetup):
        """

        This testcase covers # 13614 in Litmus
        1.Verifies custom date fields do not accept yyyy-dd-mm format

        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()

        start_date = '2011-22-04'
        end_date = ''

        feedback_pg.filter_by_custom_dates_using_keyboard(start_date, end_date)
        Assert.equal(feedback_pg.date_start_from_url, string.replace(start_date, '-', ''))
        Assert.equal(feedback_pg.date_end_from_url, '')

        Assert.equal(feedback_pg.warning, 'No search results found.')

        feedback_pg.click_custom_dates()
        Assert.equal(feedback_pg.custom_start_date, string.replace(start_date, '-', ''))
        Assert.equal(feedback_pg.custom_end_date, '')
        Assert.equal(feedback_pg.custom_date_only_error, 'Enter a valid date.')
