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


from unittestzero import Assert

from datetime import date
from pages.desktop.feedback import FeedbackPage


class TestDatePicker:

    def test_datepicker_is_only_shown_when_a_date_field_has_focus(self, mozwebqa):
        """

        This testcase covers # 13726 in Litmus
        1.Verify that two text fields appear to set the start and end dates
        2.On clicking inside the date text field a calendar should pop up to select the date
        3.Calendar pop up gets closed
        4.Selected date is set in the date field and calendar pop up gets closed

        """
        feedback_pg = FeedbackPage(mozwebqa)

        feedback_pg.go_to_feedback_page()
        Assert.false(feedback_pg.date_filter.is_datepicker_visible)
        feedback_pg.date_filter.click_custom_dates()

        #Check that two text fields appear to set the start and end dates
        Assert.true(feedback_pg.date_filter.is_custom_start_date_visible)
        Assert.true(feedback_pg.date_filter.is_custom_end_date_visible)

        #Check if clicking inside the start/end date text field a calendar pops up
        feedback_pg.date_filter.click_start_date()
        Assert.true(feedback_pg.date_filter.is_datepicker_visible)
        #dismiss the datepicker and assert that it is not visible before clicking in the end date field
        feedback_pg.date_filter.close_datepicker()
        Assert.false(feedback_pg.date_filter.is_datepicker_visible)
        feedback_pg.date_filter.click_end_date()
        Assert.true(feedback_pg.date_filter.is_datepicker_visible)

        #Check if clicking outside of calendar pop up makes it disappear
        feedback_pg.date_filter.close_datepicker()
        Assert.false(feedback_pg.date_filter.is_datepicker_visible)

    def test_selecting_date_from_datepicker_populates_text_field(self, mozwebqa):
        """

        This testcase covers # 13844 in Litmus
        1. On clicking inside the date text field a calendar should pop up to
        select the date. Verify that selected date appears in the date field.

        """
        feedback_pg = FeedbackPage(mozwebqa)

        today_date = date.today()

        feedback_pg.go_to_feedback_page()
        feedback_pg.date_filter.click_custom_dates()
        feedback_pg.date_filter.click_start_date()
        feedback_pg.date_filter.click_day(today_date.day)
        Assert.equal(feedback_pg.date_filter.custom_start_date, today_date.strftime('%Y-%m-%d'))
        feedback_pg.date_filter.click_end_date()
        feedback_pg.date_filter.click_day(today_date.day)
        Assert.equal(feedback_pg.date_filter.custom_end_date, today_date.strftime('%Y-%m-%d'))

    def test_datepicker_next_month_button_disabled(self, mozwebqa):
        """

        This testcase covers # 13844 in Litmus
        1. The forward button of the calendar pop up is disabled if the user
        is in current month thus unable to select some future date.

        """
        feedback_pg = FeedbackPage(mozwebqa)
        feedback_pg.go_to_feedback_page()
        feedback_pg.date_filter.click_custom_dates()
        feedback_pg.date_filter.click_start_date()
        Assert.true(feedback_pg.date_filter.is_datepicker_next_month_button_disabled)

        feedback_pg.date_filter.click_end_date()
        Assert.true(feedback_pg.date_filter.is_datepicker_next_month_button_disabled)
