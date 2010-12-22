#!/usr/bin/env python

# -*- coding: utf-8 -*-

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
# Portions created by the Initial Developer are Copyright (C) 2___
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
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
Created on Nov 19, 2010
'''

from page import Page
import vars

import re
import time
import base64

page_load_timeout = vars.ConnectionParameters.page_load_timeout


class InputBasePage(Page):

    _app_name_fx              =  "firefox"
    _app_name_mb              =  "mobile"

    _fx_versions              =  ("4.0b1", "4.0b2", "4.0b3", "4.0b4", "4.0b5", "4.0b6", "4.0b7")

    _mb_versions              =  ("1.1", "1.1b1", "4.0b1", "4.0b2")

    _product_dropdown         =  "product"
    _version_dropdown         =  "version"
    
    _current_type_locator = "xpath=id('filters')//h3[text()='Type of Feedback']/following-sibling::div//a[@class='selected']"
    _type_all_locator = "css=#filters a:contains(All)"
    _type_praise_locator = "css=#filters a:contains(Praise)"
    _type_issues_locator = "css=#filters a:contains(Issues)"
    _type_suggestions_locator = "css=#filters a:contains(Suggestions)"

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
    _datepicker_day_locator_prefix = "css=.ui-datepicker-calendar td:contains("
    _datepicker_day_locator_suffix = ")"

    _feedback_praise_box      =  "praise_bar"
    _feedback_issues_box      =  "issue_bar"

    _platforms                =  ("os_win7", "os_winxp", "os_mac", "os_vista", "os_linux", "os_")

    _locales                  =  {'us' : 'loc_en-US',
                                  'germany' :'loc_de',
                                  'spain' :'loc_es',
                                  'russia' :'loc_ru',
                                  'france' :'loc_fr',
                                  'british' :'loc_en-GB',
                                  'poland' :'loc_pl',
                                  'china' :'loc_zh-CN'
                                  }

    _search_results_section    = "messages"
    _search_form               = "kw-search"
    _search_box                = "id_q"

    _previous_page_locator = "css=.pager .prev"
    _next_page_locator = "css=.pager .next"

    def __init__(self, selenium):
        """Create a new instance of the class & get the page ready for testing."""
        self.selenium = selenium
        self.selenium.open('/')
        self.selenium.window_maximize()
        self.wait_for_element_present(self._search_box)

    def get_default_selected_product(self):
        """
        returns the product selected in the filter by default
        """
        param_val = self._product_dropdown + "@data-selected"
        selected_app = self.selenium.get_attribute(param_val)
        return selected_app

    def select_prod_firefox(self):
        """
        selects Firefox from Product filter
        """
        selected_app = self.get_default_selected_product()
        if re.search(self._app_name_fx, selected_app, re.IGNORECASE) is None:
            app_label = "value=%s" % (self._app_name_fx)
            self.selenium.select(self._product_dropdown, app_label)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    def select_prod_mobile(self):
        """
        selects Mobile from Product filter
        """
        selected_app = self.get_default_selected_product()
        if re.search(self._app_name_mb, selected_app, re.IGNORECASE) is None:
            app_label = "value=%s" % (self._app_name_mb)
            self.selenium.select(self._product_dropdown, app_label)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    def get_default_selected_version(self):
        """
        returns the version selected in the filter by default
        """
        selected_ver = self.selenium.get_selected_value(self._version_dropdown)
        return selected_ver

    def select_firefox_version(self, version):
        """
        selects firefox version,4.0b1
        """
        selected_ver = self.get_default_selected_version()
        if re.search(version, selected_ver, re.IGNORECASE) is None:
            for f_ver in self._fx_versions:
                if not re.search(version, f_ver, re.IGNORECASE) is None:
                    ver_label = "value=%s" % (f_ver)
                    self.selenium.select(self._version_dropdown,ver_label)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break

    def select_mobile_version(self,version):
        """
        selects mobile version,4.0b1
        """
        selected_ver = self.get_default_selected_version()
        if re.search(version, selected_ver, re.IGNORECASE) is None:
            for m_ver in self._mb_versions:
                if not re.search(version, m_ver, re.IGNORECASE) is None:
                    ver_label = "value=%s" % (m_ver)
                    self.selenium.select(self._version_dropdown,ver_label)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break

    @property
    def current_type(self):
        """

        Returns the link text of the currently applied type filter

        """
        return self.selenium.get_text(self._current_type_locator)

    def click_type_all(self):
        """

        Clicks the 'All' type filter

        """
        self.selenium.click(self._type_all_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_type_praise(self):
        """

        Clicks the 'Praise' type filter

        """
        self.selenium.click(self._type_praise_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_type_issues(self):
        """

        Clicks the 'Issues' type filter

        """
        self.selenium.click(self._type_issues_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_type_suggestions(self):
        """

        Clicks the 'Suggestions' type filter

        """
        self.selenium.click(self._type_suggestions_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    def get_current_days(self):
        """

        Returns the link text of the currently applied days filter

        """
        if self.selenium.is_element_present(self._current_when_link_locator):
            return self.selenium.get_text(self._current_when_link_locator)
        else:
            return None

    def get_days_tooltip(self, days):
        """

        Returns the tooltip for the days link 1d/7d/30d

        """
        for time in self._when_links:
            if re.search(days,time,re.IGNORECASE) is None:
                continue
            else:
                return self.selenium.get_attribute(time + "@title")

    def click_days(self,days):
        """
        clicks 1d/7d/30d
        """
        for time in self._when_links:
            if not re.search(days, time, re.IGNORECASE) is None:
                if not self.get_current_days() == time:
                    self.selenium.click(time)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break

    def get_custom_dates_tooltip(self):
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

    def is_custom_date_filter_visible(self):
        """

        Returns True if the custom date filter form is visible

        """
        return self.selenium.is_visible(self._custom_dates_locator)

    def wait_for_datepicker_to_finish_animating(self):
        self.selenium.wait_for_condition("selenium.browserbot.getCurrentWindow().document.getElementById('ui-datepicker-div').scrollHeight == 184", 10000)

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
        self.selenium.click(self._datepicker_day_locator_prefix + str(day) + self._datepicker_day_locator_suffix)
        self.wait_for_element_not_visible(self._datepicker_locator)

    def select_date(self, target_date):
        """

        Navigates to the target month in the datepicker and clicks the target day

        """
        currentYear = int(self.selenium.get_text(self._datepicker_year_locator))
        targetYear = target_date.year
        yearDelta = targetYear - currentYear
        monthDelta = yearDelta * 12

        months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
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

    def filter_by_custom_dates(self, start_date, end_date):
        """

        Filters by a custom date range

        """
        self.click_custom_dates()
        self.click_start_date()
        self.select_date(start_date)
        self.click_end_date()
        self.select_date(end_date)
        self.selenium.click(self._set_custom_date_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_platform(self,os):
        """
        clicks Windows XP/ Android etc.
        """
        for plat in self._platforms:
            if not re.search(os, plat, re.IGNORECASE) is None:
                if not self.selenium.is_checked(plat):
                    self.selenium.click(plat)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break

    def click_feedback_praise(self):
        """
        clicks Feedback type - Praise
        """
        if not self.selenium.is_checked(self._feedback_praise_box):
            self.selenium.click(self._feedback_praise_box)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_feedback_issues(self):
        """
        clicks Feedback type - Issues
        """
        if not self.selenium.is_checked(self._feedback_issues_box):
            self.selenium.click(self._feedback_issues_box)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_locale(self,country_name):
        """
        clicks US/German/Spanish etc.
        """
        for country,loc_code in self._locales.iteritems():
            if not re.search(country_name, country, re.IGNORECASE) is None:
                if not self.selenium.is_checked(loc_code):
                    self.selenium.click(loc_code)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break

    def verify_all_firefox_versions(self):
        """
            checks all Fx versions are present
        """
        for version in self._fx_versions:
            version_locator = "css=select#%s > option[value='%s']" % (self._version_dropdown,version)
            if not (self.selenium.is_element_present(version_locator)):
                raise Exception('Version %s not found in the filter' % (version))

    def verify_all_mobile_versions(self):
        """
            checks all mobile versions are present
        """
        for version in self._mb_versions:
            version_locator = "css=select#%s > option[value='%s']" % (self._version_dropdown,version)
            if not (self.selenium.is_element_present(version_locator)):
                raise Exception('Version %s not found in the filter' % (version))

    def search_for(self, search_string):
        self.selenium.type(self._search_box, search_string)
        self.selenium.key_press(self._search_box, '\\13')
        self.selenium.wait_for_page_to_load(page_load_timeout)

    @property
    def message_count(self):
        return self.selenium.get_xpath_count('//li[@class="message"]')

    @property
    def praise_count(self):
        return self.selenium.get_xpath_count('//p[@class="type praise"]')

    @property
    def issue_count(self):
        return self.selenium.get_xpath_count('//p[@class="type issue"]')

    def click_previous_page(self):
        """

        Navigates to the previous page of results

        """
        self.selenium.click(self._previous_page_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)

    def click_next_page(self):
        """

        Navigates to the next page of results
        
        """
        self.selenium.click(self._next_page_locator)
        self.selenium.wait_for_page_to_load(page_load_timeout)
