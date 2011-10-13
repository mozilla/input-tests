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
#   Dave Hunt <dhunt@mozilla.com>
#   Alex Lakatos <alex.lakatos@softvision.ro>
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

import re

from page import Page


class DateFilter(Page):

    _current_when_link_locator = "css=#when a.selected"
    _when_links = ("link=1d", "link=7d", "link=30d")
    _show_custom_dates_locator = "id=show-custom-date"
    _custom_dates_locator = "id=custom-date"
    _custom_start_date_locator = "id=id_date_start"
    _custom_end_date_locator = "id=id_date_end"
    _set_custom_date_locator = "css=#custom-date button:contains(Set)"

    _datepicker_locator = "id=ui-datepicker-div"
    _datepicker_month_locator = "css=.ui-datepicker-month"
    _datepicker_year_locator = "css=.ui-datepicker-year"
    _datepicker_previous_month_locator = "css=.ui-datepicker-prev"
    _datepicker_next_month_locator = "css=.ui-datepicker-next"
    _datepicker_next_month_disabled_locator = "css=.ui-datepicker-next.ui-state-disabled"
    _datepicker_day_locator_prefix = "css=.ui-datepicker-calendar td:contains("
    _datepicker_day_locator_suffix = ")"

    _custom_date_only_error_locator = "//div[@id='custom-date']/ul/li"
    _custom_date_first_error_locator = "//div[@id='custom-date']/ul[1]/li"
    _custom_date_second_error_locator = "//div[@id='custom-date']/ul[2]/li"

    @property
    def current_days(self):
        """

        Returns the link text of the currently applied days filter

        """
        return self.selenium.get_text(self._current_when_link_locator)

    def get_days_tooltip(self, days):
        """

        Returns the tooltip for the days link 1d/7d/30d

        """
        for time in self._when_links:
            if re.search(days, time, re.IGNORECASE) is None:
                continue
            else:
                return self.selenium.get_attribute(time + "@title")

    def click_days(self, days):
        """
        clicks 1d/7d/30d
        """
        for time in self._when_links:
            if not re.search(days, time, re.IGNORECASE) is None:
                if not self.current_days == time:
                    self.selenium.click(time)
                    self.selenium.wait_for_page_to_load(self.timeout)
                    break

    @property
    def custom_dates_tooltip(self):
        """

        Returns the tooltip for the custom dates filter link 1d/7d/30d

        """
        return self.selenium.get_attribute(self._show_custom_dates_locator + "@title")

    def click_custom_dates(self):
        """

        Clicks the custom date filter button and waits for the form to appear

        """
        self.selenium.click(self._show_custom_dates_locator)
        self.wait_for_element_visible(self._custom_dates_locator)

    @property
    def is_custom_date_filter_visible(self):
        """

        Returns True if the custom date filter form is visible

        """
        return self.selenium.is_visible(self._custom_dates_locator)

    @property
    def is_datepicker_visible(self):
        """

        Returns True if the datepicker pop up is visible

        """
        date_picker = self.selenium.get_attribute(self._datepicker_locator + "@" + "style")
        if (date_picker.find("block") == -1):
            return False
        else:
            return True

    @property
    def is_custom_start_date_visible(self):
        """

        Returns True if the custom start date input form is visible

        """
        return self.selenium.is_visible(self._custom_start_date_locator)

    @property
    def is_custom_end_date_visible(self):
        """

        Returns True if the custom end date input form is visible

        """
        return self.selenium.is_visible(self._custom_end_date_locator)

    @property
    def is_datepicker_next_month_button_disabled(self):
        return self.selenium.is_visible(self._datepicker_next_month_disabled_locator)

    def wait_for_datepicker_to_finish_animating(self):
        self.selenium.wait_for_condition(
            "selenium.browserbot.getCurrentWindow().document.getElementById('ui-datepicker-div').scrollWidth == 251", 10000)

    def close_datepicker(self):
        self.selenium.click_at("id=body", "1,1")
        self.wait_for_element_not_visible(self._datepicker_locator)

    def click_start_date(self):
        """

        Clicks the start date in the custom date filter form and waits for the datepicker to appear

        """
        self.selenium.click(self._custom_start_date_locator)
        self.wait_for_datepicker_to_finish_animating()

    def click_end_date(self):
        """

        Clicks the end date in the custom date filter form and waits for the datepicker to appear

        """
        self.selenium.click(self._custom_end_date_locator)
        self.wait_for_datepicker_to_finish_animating()

    def click_previous_month(self):
        """

        Clicks the previous month button in the datepicker

        """
        self.selenium.click(self._datepicker_previous_month_locator)

    def click_next_month(self):
        """

        Clicks the next month button in the datepicker

        """
        # TODO: Throw an error if the next month button is disabled
        self.selenium.click(self._datepicker_next_month_locator)

    def click_day(self, day):
        """

        Clicks the day in the datepicker and waits for the datepicker to disappear

        """
        # TODO: Throw an error if the day button is disabled
        self.wait_for_element_visible(self._datepicker_day_locator_prefix + str(day) + self._datepicker_day_locator_suffix)
        self.selenium.click(self._datepicker_day_locator_prefix + str(day) + self._datepicker_day_locator_suffix)
        self.wait_for_element_not_visible(self._datepicker_locator)

    def select_date_from_datepicker(self, target_date):
        """

        Navigates to the target month in the datepicker and clicks the target day

        """
        currentYear = int(self.selenium.get_text(self._datepicker_year_locator))
        targetYear = target_date.year
        yearDelta = targetYear - currentYear
        monthDelta = yearDelta * 12

        months = {"January": 1,
                  "February": 2,
                  "March": 3,
                  "April": 4,
                  "May": 5,
                  "June": 6,
                  "July": 7,
                  "August": 8,
                  "September": 9,
                  "October": 10,
                  "November": 11,
                  "December": 12}
        currentMonth = months[self.selenium.get_text(self._datepicker_month_locator)]
        targetMonth = target_date.month
        monthDelta += targetMonth - currentMonth

        count = 0
        while (count < abs(monthDelta)):
            if monthDelta < 0:
                self.click_previous_month()
            elif monthDelta > 0:
                self.click_next_month()
            count = count + 1
        self.click_day(target_date.day)

    def set_custom_start_date_using_keyboard(self, date):
        self.click_start_date()
        self.selenium.type_keys(self._custom_start_date_locator, date)

    def set_custom_end_date_using_keyboard(self, date):
        self.click_end_date()
        self.selenium.type_keys(self._custom_end_date_locator, date)

    def set_custom_start_date_using_datepicker(self, date):
        self.click_start_date()
        self.select_date_from_datepicker(date)

    def set_custom_end_date_using_datepicker(self, date):
        self.click_end_date()
        self.select_date_from_datepicker(date)

    def filter_by_custom_dates_using_datepicker(self, start_date, end_date):
        """

        Filters by a custom date range

        """
        self.click_custom_dates()
        self.set_custom_start_date_using_datepicker(start_date)
        self.set_custom_end_date_using_datepicker(end_date)
        self.selenium.click(self._set_custom_date_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def filter_by_custom_dates_using_keyboard(self, start_date, end_date):
        """

        Filters by a custom date range using any input type, not using date() format
        This uses selenium.type_keys in an attempt to mimic actual typing

        """
        self.click_custom_dates()
        self.set_custom_start_date_using_keyboard(start_date)
        self.set_custom_end_date_using_keyboard(end_date)
        self.selenium.click(self._set_custom_date_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_days_visible(self):
        """
        Verifys if the 1d/7d/30d are visible
        """
        for time in self._when_links:
            if not self.selenium.is_visible(time):
                return False
        return True

    @property
    def is_date_filter_applied(self):
        try:
            self.date_start_from_url()
            self.date_end_from_url()
            return True
        except:
            return False

    @property
    def custom_date_only_error(self):
        return self.selenium.get_text(self._custom_date_only_error_locator)

    @property
    def custom_date_first_error(self):
        return self.selenium.get_text(self._custom_date_first_error_locator)

    @property
    def custom_date_second_error(self):
        return self.selenium.get_text(self._custom_date_second_error_locator)

    @property
    def custom_start_date(self):
        return self.selenium.get_value(self._custom_start_date_locator)

    @property
    def custom_end_date(self):
        return self.selenium.get_value(self._custom_end_date_locator)
