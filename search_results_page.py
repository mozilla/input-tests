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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
#                 David Burns
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
Created on Nov 24, 2010
'''

from urlparse import urlparse
from datetime import date, timedelta

import input_base_page
import vars

import re

page_load_timeout = vars.ConnectionParameters.page_load_timeout


class SearchResultsPage(input_base_page.InputBasePage):

    _page_title                  =  'Search Results'
    _messages_count              =  "css=div[id='big-count'] > p"
    _mobile_results_url_regexp   =  "product=mobile&version="
    _firefox_results_url_regexp  =  "product=firefox&version="
    _date_start_url_regexp  =  "date_start="
    _date_end_url_regexp  =  "date_end="

    def __init__(self, selenium):
        '''
            Creates a new instance of the class
        '''
        super(SearchResultsPage, self).__init__(selenium)

    def verify_mobile_search_page_url(self):
        """
            verifies ?product=mobile in the url
        """

        current_loc = self.selenium.get_location()
        if not self._mobile_results_url_regexp in current_loc:
            raise Exception('%s not found in %s' % (self._mobile_results_url_regexp, current_loc))

    def verify_firefox_search_page_url(self):
        """
            verifies ?product=firefox in the url
            NOTE: if the site is on the homepage (not on the search
                 page) and default/latest version is selected then
                the URL will not contain product=firefox&version=
        """
        if re.search(self._page_title, self.selenium.get_title(), re.I) is None:
            return
        current_loc = self.selenium.get_location()
        if not self._firefox_results_url_regexp in current_loc:
            raise Exception('%s not found in %s' % (self._firefox_results_url_regexp, current_loc))

    def verify_search_form_prod_ver(self, prod, ver):
        """
            verifies:
            product=firefox in <input type="hidden" value="firefox" name="product">
            and
            version=4.0b6 in <input type="hidden" value="4.0b6" name="version">

            NOTE: if the site is on the homepage (not on the search
                 page) and default/latest version is selected for Fx
                 then <input type="hidden" value="4.0b7" name="version">
                will not exist
        """

        prod_tag = "css=form[id='%s'] > input[value='%s']" % (self._search_form, prod)
        ver_tag  = "css=form[id='%s'] > input[value='%s']" % (self._search_form, ver)

        if re.search(self._page_title, self.selenium.get_title(), re.I) is None:
            return

        if not self.selenium.is_element_present(prod_tag):
            raise Exception('%s not found in %s' % (prod_tag, self.selenium.get_location()))

        if not self.selenium.is_element_present(ver_tag):
            raise Exception('%s not found in %s' % (ver_tag, self.selenium.get_location()))

    @property
    def type_from_url(self):
        """

            Returns the type from the current location URL

        """

        url = urlparse(self.selenium.get_location())
        params = dict([part.split('=') for part in url[4].split('&')])
        return params["s"]

    def verify_preset_days_search_page_url(self, days):
        """

            Verifies date_start=(today - days) in the url

        """

        date_start = date.today() - timedelta(days=days)
        # The regular expression for a date when using preset filters is different to using the custom search. See bug 616306 for details.
        date_start_url_regexp = self._date_start_url_regexp + date_start.strftime('%Y-%m-%d')

        current_loc = self.selenium.get_location()
        if date_start_url_regexp in current_loc:
            pass
        else:
            raise Exception('%s not found in %s' % (date_start_url_regexp, current_loc))

    def verify_custom_dates_search_page_url(self, start_date, end_date):
        """

            Verifies date_start=(start_date) in the url
            Verifies date_end=(end_date) in the url

        """

        # The regular expression for a date when using preset filters is different to using the custom search. See bug 616306 for details.
        date_start_url_regexp = self._date_start_url_regexp + start_date.strftime('%m%%2F%d%%2F%Y')
        date_end_url_regexp = self._date_end_url_regexp + end_date.strftime('%m%%2F%d%%2F%Y')

        current_loc = self.selenium.get_location()
        if date_start_url_regexp in current_loc:
            pass
        else:
            raise Exception('%s not found in %s' % (date_start_url_regexp, current_loc))

        if date_end_url_regexp in current_loc:
            pass
        else:
            raise Exception('%s not found in %s' % (date_end_url_regexp, current_loc))
