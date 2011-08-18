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

import pytest
xfail = pytest.mark.xfail
from unittestzero import Assert

import feedback_page


class Test_Feedback_Layout:

    """
    Litmus 13593 - input:Verify the layout of homepage
    """
    def test_the_header_layout(self, testsetup):
        """
        Litmus 13594 - input:Verify the layout of header area
        Litmus 13599 - input:Check the links in header area
        """
        base_page = feedback_page.FeedbackPage(testsetup)
        base_page.go_to_feedback_page()

        header = base_page.header_region

        feedback_pg = header.click_feedback_link()
        Assert.true(feedback_pg.is_the_current_page)
        base_page.go_to_feedback_page()

        themes = header.click_themes_link()
        Assert.true(themes.is_the_current_page)
        base_page.go_to_feedback_page()

        sites = header.click_sites_link()
        Assert.true(sites.is_the_current_page)
        base_page.go_to_feedback_page()

        feedback_pg = header.click_main_heading_link()
        Assert.true(feedback_pg.is_the_current_page)

    def test_the_area_layout(self, testsetup):
        """
        Litmus 13598 - input:Verify the layout of footer area
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        footer = feedback_pg.footer_region

        Assert.equal(footer.privacy_policy, "Privacy Policy")

        Assert.equal(footer.legal_notices, "Legal Notices")

        Assert.equal(footer.report_trademark_abuse, "Report Trademark Abuse")

        Assert.equal(footer.unless_otherwise_noted, "noted")

        Assert.equal(footer.creative_commons, "Creative Commons Attribution Share-Alike License v3.0")

        Assert.equal(footer.about_input, "About Firefox Input")

        Assert.true(footer.is_language_dropdown_visible)

    def test_the_left_panel_layout(self, testsetup):
        """
        Litmus 13595 - input:Verify the layout of the left hand side section containing various
        filtering options
        Litmus 13600 - input:Verify the applications drop down in Product
        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.true(feedback_pg.product_filter.default_values("firefox", "6.0"))
        Assert.false(feedback_pg.date_filter.is_date_filter_applied)

        Assert.false(feedback_pg.date_filter.is_custom_date_filter_visible)

        feedback_pg.date_filter.click_custom_dates()

        Assert.true(feedback_pg.platform_filter.platform_count > 0)
        Assert.equal(feedback_pg.product_filter.products, ['Firefox', 'Mobile'])
        feedback_pg.product_filter.select_version('--')
        types = [type.name for type in feedback_pg.type_filter.types()]
        Assert.equal(types, ['Praise', 'Issues', 'Ideas'])

        platforms = [platform.name for platform in feedback_pg.platform_filter.platforms()]
        Assert.equal(platforms, ['Windows 7', 'Windows XP', 'Windows Vista', 'Mac OS X', 'Linux'])

        Assert.true(feedback_pg.locale_filter.locale_count > 0)

        locales = [locale.name for locale in feedback_pg.locale_filter.locales()]
        Assert.true(set(['English (US)', 'German', 'Spanish', 'French']).issubset(set(locales)))

    @xfail(reason="Bug 664562 - [stage] [prod] View older marks does not redirect to page=2")
    def test_the_middle_section_page(self, testsetup):
        """
        Litmus 13596 - input:Verify the layout of Latest Feedback section
        Litmus 13721 - input:Verify the layout of Feedback page(Feedback tab)
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.equal(feedback_pg.search_box_placeholder, "Search by keyword")
        Assert.true(feedback_pg.message_count > 0)

        Assert.true(feedback_pg.is_chart_visible)

        Assert.true(feedback_pg.is_next_page_enabled)
        Assert.false(feedback_pg.is_previous_page_enabled)

        #the first click only applies the filters and add messages until the message count reaches 20
        #the second click goes to the next page
        #this is discussed in bug https://bugzilla.mozilla.org/show_bug.cgi?id=640007

        feedback_pg.click_next_page()
        feedback_pg.click_next_page()

        Assert.true(feedback_pg.is_next_page_enabled)
        Assert.true(feedback_pg.is_previous_page_enabled)

        feedback_pg.click_previous_page()

        Assert.true(feedback_pg.is_next_page_visible)
        Assert.false(feedback_pg.is_previous_page_enabled)

    @xfail(reason="Bug 659640 - [Input] 'While visiting' section is not shown on the homepage")
    def test_the_right_panel_layout(self, testsetup):
        """
        Litmus 13597 - input:Verify the layout of right hand section containing statistics data
        Litmus 13716 - input:Verify while visiting section
        """

        feedback_pg = feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        Assert.equal(feedback_pg.total_message_count_heading, "Messages")
        Assert.true(feedback_pg.total_message_count > 0)

        Assert.equal(feedback_pg.common_words_filter.common_words_header, "Often Mentioned")
        Assert.true(feedback_pg.common_words_filter.common_words_count > 0)

        Assert.equal(feedback_pg.sites_filter.sites_filter_header, "While Visiting")
        Assert.true(feedback_pg.sites_filter.sites_filter_count > 0)
