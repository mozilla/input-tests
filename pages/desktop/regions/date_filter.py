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

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from page import Page


class DateFilter(Page):

    _current_when_link_locator = (By.CSS_SELECTOR, '#when a.selected')
    _last_day_locator = (By.LINK_TEXT, '1d')
    _last_seven_days_locator = (By.LINK_TEXT, '7d')
    _last_thirty_days_locator = (By.LINK_TEXT, '30d')
    _show_custom_dates_locator = (By.ID, 'show-custom-date')
    _custom_dates_locator = (By.ID, 'custom-date')
    _custom_start_date_locator = (By.ID, 'id_date_start')
    _custom_end_date_locator = (By.ID, 'id_date_end')
    _set_custom_date_locator = (By.CSS_SELECTOR, '#custom-date button')

    _datepicker_locator = (By.ID, 'ui-datepicker-div')
    _datepicker_calendar_locator = (By.CSS_SELECTOR, '.ui-datepicker-calendar')
    _datepicker_month_locator = (By.CSS_SELECTOR, '.ui-datepicker-month')
    _datepicker_year_locator = (By.CSS_SELECTOR, '.ui-datepicker-year')
    _datepicker_previous_month_locator = (By.CSS_SELECTOR, '.ui-datepicker-prev')
    _datepicker_next_month_locator = (By.CSS_SELECTOR, '.ui-datepicker-next')
    _datepicker_next_month_disabled_locator = (By.CSS_SELECTOR, '.ui-datepicker-next.ui-state-disabled')

    _custom_date_only_error_locator = (By.XPATH, "//div[@id='custom-date']/ul/li")
    _custom_date_first_error_locator = (By.XPATH, "//div[@id='custom-date']/ul[1]/li")
    _custom_date_second_error_locator = (By.XPATH, "//div[@id='custom-date']/ul[2]/li")

    @property
    def current_days(self):
        """Returns the link text of the currently applied days filter."""
        return self.selenium.find_element(*self._current_when_link_locator).text

    @property
    def last_day_tooltip(self):
        return self.selenium.find_element(*self._last_day_locator).get_attribute('title')

    @property
    def last_seven_days_tooltip(self):
        return self.selenium.find_element(*self._last_seven_days_locator).get_attribute('title')

    @property
    def last_thirty_days_tooltip(self):
        return self.selenium.find_element(*self._last_thirty_days_locator).get_attribute('title')

    def click_last_day(self):
        return self.selenium.find_element(*self._last_day_locator).click()

    def click_last_seven_days(self):
        return self.selenium.find_element(*self._last_seven_days_locator).click()

    def click_last_thirty_days(self):
        return self.selenium.find_element(*self._last_thirty_days_locator).click()

    @property
    def custom_dates_tooltip(self):
        """Returns the tooltip for the custom dates filter link."""
        return self.selenium.find_element(*self._show_custom_dates_locator).get_attribute('title')

    def click_custom_dates(self):
        """Clicks the custom date filter button and waits for the form to appear."""
        self.selenium.find_element(*self._show_custom_dates_locator).click()

    @property
    def is_custom_date_filter_visible(self):
        """Returns True if the custom date filter form is visible."""
        return self.is_element_visible(self._custom_dates_locator)

    @property
    def is_datepicker_visible(self):
        """Returns True if the datepicker pop up is visible."""
        datepicker = self.selenium.find_element(*self._datepicker_locator)
        return datepicker.is_displayed() and datepicker.location['x'] > 0

    @property
    def is_custom_start_date_visible(self):
        """Returns True if the custom start date input form is visible."""
        return self.is_element_visible(self._custom_start_date_locator)

    @property
    def is_custom_end_date_visible(self):
        """Returns True if the custom end date input form is visible."""
        return self.is_element_visible(self._custom_end_date_locator)

    @property
    def is_datepicker_next_month_button_disabled(self):
        return self.is_element_visible(self._datepicker_next_month_disabled_locator)

    def wait_for_datepicker_to_open(self):
        WebDriverWait(self.selenium, 3).until(lambda s: self.is_datepicker_visible)
        WebDriverWait(self.selenium, 3).until(lambda s: s.find_element(*self._datepicker_locator).size['width'] == 251)

    def wait_for_datepicker_to_close(self):
        WebDriverWait(self.selenium, 3).until(lambda s: not self.is_datepicker_visible)

    def close_datepicker(self):
        self.selenium.find_element(*self._custom_start_date_locator).send_keys(Keys.ESCAPE)
        WebDriverWait(self.selenium, 3).until(lambda s: not self.is_datepicker_visible)

    def click_start_date(self):
        """Clicks the start date in the custom date filter form and waits for the datepicker to appear."""
        self.selenium.find_element(*self._custom_start_date_locator).click()
        self.wait_for_datepicker_to_open()

    def click_end_date(self):
        """Clicks the end date in the custom date filter form and waits for the datepicker to appear."""
        self.selenium.find_element(*self._custom_end_date_locator).click()
        self.wait_for_datepicker_to_open()

    def click_previous_month(self):
        """Clicks the previous month button in the datepicker."""
        self.selenium.find_element(*self._datepicker_previous_month_locator).click()

    def click_next_month(self):
        """Clicks the next month button in the datepicker."""
        # TODO: Throw an error if the next month button is disabled
        self.selenium.find_element(*self._datepicker_next_month_locator).click()

    def click_day(self, day):
        """Clicks the day in the datepicker and waits for the datepicker to disappear."""
        # TODO: Throw an error if the day button is disabled
        calendar = self.selenium.find_element(*self._datepicker_calendar_locator)
        calendar.find_element(By.LINK_TEXT, str(day)).click()
        self.wait_for_datepicker_to_close()

    def select_date_from_datepicker(self, target_date):
        """Navigates to the target month in the datepicker and clicks the target day."""
        currentYear = int(self.selenium.find_element(*self._datepicker_year_locator).text)
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
        currentMonth = months[self.selenium.find_element(*self._datepicker_month_locator).text]
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

    def type_custom_start_date(self, date):
        self.selenium.find_element(*self._custom_start_date_locator).send_keys(date)

    def type_custom_end_date(self, date):
        self.selenium.find_element(*self._custom_end_date_locator).send_keys(date)

    def select_custom_start_date_using_datepicker(self, date):
        self.click_start_date()
        self.select_date_from_datepicker(date)

    def select_custom_end_date_using_datepicker(self, date):
        self.click_end_date()
        self.select_date_from_datepicker(date)

    def filter_by_custom_dates_using_datepicker(self, start_date, end_date):
        """Filters by a custom date range."""
        self.click_custom_dates()
        self.select_custom_start_date_using_datepicker(start_date)
        self.select_custom_end_date_using_datepicker(end_date)
        self.selenium.find_element(*self._set_custom_date_locator).click()

    def filter_by_custom_dates_using_keyboard(self, start_date, end_date):
        """Filters by a custom date range using any input type, not using date() format.

        This uses selenium.type_keys in an attempt to mimic actual typing

        """
        self.click_custom_dates()
        self.type_custom_start_date(start_date)
        self.type_custom_end_date(end_date)
        self.selenium.find_element(*self._set_custom_date_locator).click()

    @property
    def is_last_day_visible(self):
        return self.is_element_visible(self._last_day_locator)

    @property
    def is_last_seven_days_visible(self):
        return self.is_element_visible(self._last_seven_days_locator)

    @property
    def is_last_thirty_days_visible(self):
        return self.is_element_visible(self._last_thirty_days_locator)

    @property
    def is_date_filter_applied(self):
        from pages.base import BasePage
        base = BasePage(self.testsetup)
        return base.date_start_from_url and base.date_end_from_url or False

    @property
    def custom_date_only_error(self):
        return self.selenium.find_element(*self._custom_date_only_error_locator).text

    @property
    def custom_date_first_error(self):
        return self.selenium.find_element(*self._custom_date_first_error_locator).text

    @property
    def custom_date_second_error(self):
        return self.selenium.find_element(*self._custom_date_second_error_locator).text

    @property
    def custom_start_date(self):
        return self.selenium.find_element(*self._custom_start_date_locator).get_attribute('value')

    @property
    def custom_end_date(self):
        return self.selenium.find_element(*self._custom_end_date_locator).get_attribute('value')
