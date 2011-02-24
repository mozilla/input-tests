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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
#                 Dave Hunt <dhunt@mozilla.com>
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

    _mobile_versions = ("4.0b1", "4.0b2", "4.0b3")

    _product_dropdown_locator = "id=product"
    _version_dropdown_locator = "id=version"

    _type_all_locator = "css=#filters a:contains(All)"
    _type_praise_locator = "css=#filters a:contains(Praise)"
    _type_issues_locator = "css=#filters a:contains(Issues)"
    _type_ideas_locator = "css=#filters a:contains(Ideas)"

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
    _more_locales_link_locator = "css=#filter_locale .more"
    _locales_locator = "//div[@id='filter_locale']/ul[@class='bars']/div[1]/li"
    _extra_locales_locator = "css=#filter_locale .extra"
    _extra_locales_xpath_locator = "//div[@id='filter_locale']/ul[@class='bars']/div[@class='extra']/li"
    _first_message_locale_locator = "//li[@class='message'][1]/ul/li[3]/a"
    _search_results_section    = "messages"
    _search_form               = "kw-search"
    _search_box                = "id_q"

    _previous_page_locator = "css=.pager .prev"
    _next_page_locator = "css=.pager .next"

    def __init__(self, selenium):
        self.selenium = selenium
        self.selenium.window_maximize()

    @property
    def products(self):
        """
        returns a list of available products
        """
        return self.selenium.get_select_options(self._product_dropdown_locator)

    @property
    def selected_product(self):
        """
        returns the currently selected product
        """
        self.wait_for_element_present(self._product_dropdown_locator)
        return self.selenium.get_selected_value(self._product_dropdown_locator)

    def select_product(self, product):
        """
        selects product
        """
        if not product == self.selected_product:
            self.selenium.select(self._product_dropdown_locator, "value=" + product)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    @property
    def versions(self):
        """
        returns a list of available versions
        """
        return self.selenium.get_select_options(self._version_dropdown_locator)

    def selected_version(self, type='value'):
        """
        returns the currently selected product version
        """
        return getattr(self.selenium, "get_selected_" + type)(self._version_dropdown_locator)

    def select_version(self, lookup, by='value'):
        """
        selects product version
        """
        if not lookup == self.selected_version(by):
            self.selenium.select(self._version_dropdown_locator, by + "=" + str(lookup))
            self.selenium.wait_for_page_to_load(page_load_timeout)

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

    def click_type_ideas(self):
        """

        Clicks the 'Ideas' type filter

        """
        self.selenium.click(self._type_ideas_locator)
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
        self.selenium.wait_for_condition("selenium.browserbot.getCurrentWindow().document.getElementById('ui-datepicker-div').scrollWidth == 251", 10000)

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

    def click_locale(self,lookup, by="name"):
        """
        clicks US/German/Spanish etc.
        """
        if by == "name":
            for country,loc_code in self._locales.iteritems():
                if not re.search(lookup, country, re.IGNORECASE) is None:
                    if not self.selenium.is_checked(loc_code):
                        self.selenium.click(loc_code)
                        self.selenium.wait_for_page_to_load(page_load_timeout)
                        break
        elif by == "index":
            if lookup <= 10:
                self.selenium.click(self._locales_locator+"["+str(lookup)+"]/input")
            else:
                self.selenium.click(self._extra_locales_xpath_locator+"["+str(lookup-10)+"]/input")
            self.selenium.wait_for_page_to_load(page_load_timeout)

    def locale_name_by_index(self, index):
        """
        returns a locale name by index
        """
        if index <= 10:
            return self.selenium.get_text(self._locales_locator+"["+str(index)+"]/label/strong")
        else:
            return self.selenium.get_text(self._extra_locales_xpath_locator+"["+str(index-10)+"]/label/strong")

    def locale_code_by_index(self, index):
        """
        returns the locale code by index
        """
        if index <= 10:
            return self.selenium.get_attribute(self._locales_locator+"["+str(index)+"]/input@value")
        else:
            return self.selenium.get_attribute(self._extra_locales_xpath_locator+"["+str(index-10)+"]/input@value")

    def locale_message_count(self, lookup, by="index"):
        """
        Returns the number of messages for a locale in the locales list
        """
        if by == "index":
            if lookup <= 10:
                return int(self.selenium.get_text(self._locales_locator+"["+str(lookup)+"]/label/span[@class='count']"))
            else:
                return int(self.selenium.get_text(self._extra_locales_xpath_locator+"["+str(lookup-10)+"]/label/span[@class='count']"))
        if by == "name":
            return int(self.selenium.get_text(self._locales_locator+"/label[@for='loc_"+lookup+"']/span[@class='count']"))

    def click_more_locales_link(self):
        """
        clicks the 'More locales' link
        """
        self.selenium.click(self._more_locales_link_locator)
        self.wait_for_element_not_visible(self._more_locales_link_locator)
        self.wait_for_element_visible(self._extra_locales_locator)

    @property
    def first_message_locale(self):
        """
        Returns the locale name for the first message in the message list
        """
        return self.selenium.get_text(self._first_message_locale_locator)

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
        for version in self._mobile_versions:
            version_locator = "css=select#%s > option[value='%s']" % (self._version_dropdown,version)
            if not (self.selenium.is_element_present(version_locator)):
                raise Exception('Version %s not found in the filter' % (version))

    def search_for(self, search_string):
        self.selenium.type(self._search_box, search_string)
        self.selenium.key_press(self._search_box, '\\13')
        self.selenium.wait_for_page_to_load(page_load_timeout)

    @property
    def message_count(self):
        return int(self.selenium.get_xpath_count('//li[@class="message"]'))

    @property
    def praise_count(self):
        return self.selenium.get_xpath_count('//p[@class="type praise"]')

    @property
    def issue_count(self):
        return self.selenium.get_xpath_count('//p[@class="type issue"]')

    @property
    def locale_count(self):
        return int(self.selenium.get_xpath_count(self._locales_locator))

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
