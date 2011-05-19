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
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
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

"""
Litmus 13593 - input:Verify the layout of homepage
"""

import pytest
xfail = pytest.mark.xfail
from unittestzero import Assert

import feedback_page


class Test_Feedback_Layout:

    def test_the_heder_layout(self, testsetup):
        """
        Litmus 13594 - input:Verify the layout of header area
        Litmus 13599 - input:Check the links in header area
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.true(feedback_pg.is_feedback_link_visible)
        feedback_pg.click_feedback_link()
        Assert.equal(feedback_pg.title, "Welcome :: Firefox Input")

        Assert.true(feedback_pg.is_themes_link_visible)
        feedback_pg.click_themes_link()
        Assert.equal(feedback_pg.title, "Themes :: Firefox Input")
        feedback_pg.go_back()

        Assert.true(feedback_pg.is_sites_link_visible)
        feedback_pg.click_sites_link()
        Assert.equal(feedback_pg.title, "Sites :: Firefox Input")
        feedback_pg.go_back()

        Assert.true(feedback_pg.is_main_heading_link_visible)
        feedback_pg.click_main_heading_link()
        Assert.equal(feedback_pg.title, "Welcome :: Firefox Input")

    def test_the_footer_area_layout(self, testsetup):
        """
        Litmus 13598 - input:Verify the layout of footer area
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.true(feedback_pg.is_footer_privacy_policy_visible)
        Assert.equal(feedback_pg.footer_privacy_policy, "Privacy Policy")
        Assert.true(feedback_pg.is_footer_legal_notices_visible)
        Assert.equal(feedback_pg.footer_legal_notices, "Legal Notices")
        Assert.true(feedback_pg.is_footer_report_trademark_abuse_link_visible)
        Assert.equal(feedback_pg.footer_report_trademark_abuse, "Report Trademark Abuse")
        Assert.true(feedback_pg.is_footer_unless_otherwise_noted_visible)
        Assert.equal(feedback_pg.footer_unless_otherwise_noted, "noted")
        Assert.true(feedback_pg.is_footer_creative_commons_link_visible)
        Assert.equal(feedback_pg.footer_creative_commons, "Creative Commons Attribution Share-Alike License v3.0")
        Assert.true(feedback_pg.is_footer_about_input_visible)
        Assert.equal(feedback_pg.footer_about_input, "About Firefox Input")

        Assert.true(feedback_pg.is_footer_language_dropdown_visible)

    def test_the_left_panel_layout(self, testsetup):
        """
        Litmus 13595 - input:Verify the layout of the left hand side section containing various
        filtering options
        Litmus 13600 - input:Verify the applications drop down in Product
        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.true(feedback_pg.product_filter.verify_location)
        Assert.true (feedback_pg.is_days_visible)

        feedback_pg.click_custom_dates()

        Assert.true(feedback_pg.is_custom_date_filter_visible())

        Assert.not_equal(feedback_pg.platform_filter.platform_count, 0)
        Assert.equal (feedback_pg.product_filter.products , [u'Firefox', u'Mobile'])

        type_enum = ("Praise",
                    "Issues",
                    "Ideas")
        for type in type_enum:
            Assert.true(feedback_pg.type_filter.contains_type(type))

        platform_names = ("Windows 7",
                         "Windows XP",
                         "Windows Vista",
                         "Mac OS X",
                         "Linux")

        for lock in platform_names:
            Assert.true(feedback_pg.platform_filter.contains_platform(lock))

        Assert.not_equal(feedback_pg.locale_filter.locale_count, 0)

        locale_names = ("English (US)",
                        "German",
                        "Spanish",
                        "French")

        for lock in locale_names:
            Assert.true(feedback_pg.locale_filter.contains_locale(lock))

    def test_the_middle_section_page(self, testsetup):
        """
        Litmus 13596 - input:Verify the layout of Latest Feedback section
        Litmus 13721 - input:Verify the layout of Feedback page(Feedback tab)
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.equal(feedback_pg.search_box_placeholder(), "Search by keyword")
        Assert.not_equal(feedback_pg.message_count, 0)

        Assert.true(feedback_pg.is_chart_visible)

        Assert.true(feedback_pg.is_next_page_visible)
        Assert.true(feedback_pg.is_previous_page_visible)
        #this is is "intended"
        feedback_pg.click_next_page()
        feedback_pg.click_next_page()

        Assert.true(feedback_pg.is_next_page_visible)
        Assert.true(feedback_pg.is_previous_page_visible)

        feedback_pg.click_previous_page()

        Assert.true(feedback_pg.is_next_page_visible)
        Assert.true(feedback_pg.is_previous_page_visible)

    def test_the_right_panel_layout(self, testsetup):
        """
        Litmus 13597 - input:Verify the layout of right hand section containing statistics data
        Litmus 13716 - input:Verify while visiting section
        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.equal(feedback_pg.total_message_count_heading, "Messages")
        Assert.not_equal(feedback_pg.total_message_count, 0)

        Assert.equal(feedback_pg.mentioned_filter.mentioned_header, "Often Mentioned Toggle")
        Assert.not_equal(feedback_pg.mentioned_filter.mentioned_count, 0)

        Assert.equal(feedback_pg.visiting_filter.visiting_header , "While Visiting Toggle")
        Assert.not_equal(feedback_pg.visiting_filter.visiting_count, 0)
