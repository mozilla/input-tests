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
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Tobias Markus <tobbi.bugs@googlemail.com>
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


from unittestzero import Assert

import feedback_page


class TestLocaleFilter:

    def test_feedback_can_be_filtered_by_locale(self, testsetup):
        """
        This testcase covers # 15120 in Litmus
        1. Verify that the number of messages in the locale list matches the number of messages returned
        2. Verify that the locale short code appears in the URL
        3. Verify that the locale for all messages on the first page of results is correct
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product('firefox')
        feedback_pg.product_filter.select_version('--')

        locale_name = "Russian"
        locale = feedback_pg.locale_filter.locale(locale_name)
        locale_message_count = locale.message_count
        locale_code = locale.code
        locale.select()

        Assert.equal(feedback_pg.total_message_count.replace(',', ''), locale_message_count)
        Assert.equal(feedback_pg.locale_from_url, locale_code)
        [Assert.equal(message.locale, locale_name) for message in feedback_pg.messages]

    def test_feedback_can_be_filtered_by_locale_from_expanded_list(self, testsetup):
        """
        This testcase covers # 15087 & 15120 in Litmus
        1. Verify the initial locale count is 10
        2. Verify clicking the more locales link shows additional locales
        3. Verify filtering by one of the additional locales
        4. Verify that the number of messages in the locale list matches the number of messages returned
        5. Verify that the locale short code appears in the URL
        6. Verify that the locale for all messages on the first page of results is correct
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product('firefox')
        feedback_pg.product_filter.select_version('--')

        Assert.equal(feedback_pg.locale_filter.locale_count, 10)
        feedback_pg.locale_filter.show_extra_locales()
        Assert.true(feedback_pg.locale_filter.locale_count > 10)

        locale = feedback_pg.locale_filter.locale(11)
        locale_name = locale.name
        locale_message_count = locale.message_count
        locale_code = locale.code
        locale.select()

        Assert.equal(feedback_pg.total_message_count.replace(',', ''), locale_message_count)
        Assert.equal(feedback_pg.locale_from_url, locale_code)
        [Assert.equal(message.locale, locale_name) for message in feedback_pg.messages]
