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
# The Original Code is Firefox Input
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Soren Jones
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
Created on Mar 8, 2011
'''

from selenium import selenium
from vars import ConnectionParameters
import unittest
import pytest
xfail = pytest.mark.xfail

import feedback_page

class TestTypeFilters(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    @xfail(reason= 'Bug 640549 - Legend text for "Ideas" changes to "Idea" on the search page')
    def test_type_filter_names_are_the_same_in_the_filter_bar_and_the_chart(self):
        """

        1. Verify that the type names in the filter bar match the type names
           in the chart legend on the base page
        2. Verify that the type names in the filter bar match the type names
           in the chart legend on the search results page

        """
        feedback_pg = feedback_page.FeedbackPage(self.selenium)

        feedback_pg.go_to_feedback_page()
        print "Checking " + self.selenium.get_title()
        for type_filter in feedback_pg.type_filters:
            print type_filter.name + ":",
            self.failUnless(self.selenium.is_element_present(type_filter.chart_locator))
            print "OK"
        feedback_pg.search_for('')
        print "Checking " + self.selenium.get_title()
        for type_filter in feedback_pg.type_filters:
            print type_filter.name + ":",
            self.failUnless(self.selenium.is_element_present(type_filter.chart_locator))
            print "OK"

if __name__ == "__main__":
    unittest.main()
