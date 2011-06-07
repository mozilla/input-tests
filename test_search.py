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
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#                 Dave Hunt <dhunt@mozilla.com>
#                 Matt Brandt <mbrandt@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
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

import feedback_page


class TestSearch:

    def test_that_empty_search_of_feedback_returns_some_data(self, testsetup):
        '''
            Litmus 13847
        '''
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        feedback_pg.search_for('')
        Assert.true(0 < feedback_pg.message_count)

    def test_that_we_can_search_feedback_with_unicode(self, testsetup):
        '''
            Litmus 13697
        '''
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        # Select the Firefox version that is 1 less than the newest to ensure the unicode
        # search returns at least 1 result.
        feedback_pg.product_filter.select_product('firefox')
        feedback_pg.product_filter.select_version('--')

        feedback_pg.search_for(u"rapidit\xe9")
        Assert.true(0 < feedback_pg.message_count)

    def test_search_box_default_text(self, testsetup):
        '''
            Litmus 13845
        1. Verify that there is a search field appearing in Latest Feedback
        section it shows by default "Search by keyword"
        '''
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        Assert.equal(feedback_pg.search_box_placeholder, "Search by keyword")

    def test_search_box_text_disappears_on_click(self, testsetup):
        '''
            Litmus 13846
        1. Verify that on clicking in the text field default text
        "Search by keyword" disappears
        '''
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        feedback_pg.click_search_box()
        Assert.equal(feedback_pg.search_box, "")
