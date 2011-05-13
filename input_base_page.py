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
# Portions created by the Initial Developer are Copyright (C) 2011
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
from urlparse import urlparse

from page import Page


class InputBasePage(Page):

    _previous_page_locator = "css=.pager .prev"
    _next_page_locator = "css=.pager .next"

    def click_previous_page(self):
        """
        Navigates to the previous page of results
        """
        self.selenium.click(self._previous_page_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_next_page(self):
        """
        Navigates to the next page of results
        """
        self.selenium.click(self._next_page_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def _value_from_url(self, param):
        """
        Returns the value for the specified parameter in the URL
        """
        url = urlparse(self.selenium.get_location())
        params = dict([part.split('=') for part in url[4].split('&')])
        return params[param]

    @property
    def feedback_type_from_url(self):
        """
        Returns the feedback type (praise, issues, ideas) from the current location URL
        """
        return self._value_from_url("s")

    @property
    def platform_from_url(self):
        """
        Returns the platform from the current location URL
        """
        return self._value_from_url("platform")

    @property
    def product_from_url(self):
        """
        Returns the product from the current location URL
        NOTE: if the site is on the homepage (not on the search
            page) and default/latest version is selected then
            the URL will not contain the product parameter
        """
        return self._value_from_url("product")

    @property
    def version_from_url(self):
        """
        Returns the version from the current location URL
        NOTE: if the site is on the homepage (not on the search
            page) and default/latest version is selected then
            the URL will not contain the version parameter
        """
        return self._value_from_url("version")

    @property
    def date_start_from_url(self):
        """
        Returns the date_start value from the current location URL
        """
        return self._value_from_url("date_start")

    @property
    def date_end_from_url(self):
        """
        Returns the date_end value from the current location URL
        """
        return self._value_from_url("date_end")

    @property
    def page_from_url(self):
        """
        Returns the page value from the current location URL
        """
        return self._value_from_url("page")

    @property
    def locale_from_url(self):
        """
        Returns the locale value from the current location URL
        """
        return self._value_from_url("locale")
