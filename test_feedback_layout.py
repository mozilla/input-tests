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

from selenium import selenium
from vars import ConnectionParameters
import unittest


import feedback_page

class Test_Feedback_Layout(unittest.TestCase):


    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                                 ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()
        self.selenium.set_timeout(ConnectionParameters.page_load_timeout)

    def tearDown(self):
        self.selenium.stop()

    """
    Litmus 13594 - input:Verify the layout of header area
    Litmus 13599 - input:Check the links in header area
    """

    def test_the_heder_layout(self):
        feedback_pg = feedback_page.FeedbackPage(self.selenium)
        feedback_pg.go_to_feedback_page()

        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_firefox_link))
        self.assertEqual(feedback_pg.get_atribute(feedback_pg.get_firefox_link, "href"),
                        "/en-US/")
        feedback_pg.click_and_check(feedback_pg.get_firefox_link,"Welcome :: Firefox Input")

        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_themes_link))
        self.assertEqual(feedback_pg.get_atribute(feedback_pg.get_themes_link, "href"),
                         "/en-US/themes")
        feedback_pg.click_and_check(feedback_pg.get_themes_link,"Themes :: Firefox Input")
        feedback_pg.go_back()

        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_feedback_link))
        self.assertEqual(feedback_pg.get_atribute(feedback_pg.get_feedback_link, "href"),
                         "/en-US/")
        feedback_pg.click_and_check(feedback_pg.get_feedback_link,"Welcome :: Firefox Input")

        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_sites_link))
        self.assertEqual(feedback_pg.get_atribute(feedback_pg.get_sites_link, "href"),
                         "/en-US/sites")
        feedback_pg.click_and_check(feedback_pg.get_sites_link,"Sites :: Firefox Input")
        feedback_pg.go_back()


    """
    Litmus 13595 - input:Verify the layout of the left hand side section containing various
    filtering options
    """
    def test_the_left_panel_layout(self):

        feedback_pg = feedback_page.FeedbackPage(self.selenium)
        feedback_pg.go_to_feedback_page()

        self.assertTrue( feedback_pg.product_filter.verify_location)
        self.assertTrue (feedback_pg.is_days_visible)

        feedback_pg.click_custom_dates()

        self.assertTrue(feedback_pg.is_custom_date_filter_visible())

        self.assertNotEqual(feedback_pg.platform_filter.platform_count,0)
        
        platform_names = ("Windows 7",
                         "Windows XP",
                         "Windows Vista",
                         "Mac OS X",
                         "Linux")
        for lock in platform_names:
            self.assertTrue(feedback_pg.platform_filter.contains_platform(lock))

        self.assertNotEqual(feedback_pg.locale_filter.locale_count,0)

        locale_names = ("English (US)",
                        "German",
                        "Spanish",
                        "French")

        for lock in locale_names:
            self.assertTrue( feedback_pg.locale_filter.contains_locale(lock))



    """
    Litmus 13596 - input:Verify the layout of Latest Feedback section
    Litmus 13721 - input:Verify the layout of Feedback page(Feedback tab)
    """

    def test_the_feedback_page(self):

        feedback_pg = feedback_page.FeedbackPage(self.selenium)
        feedback_pg.go_to_feedback_page()
        #TODO fails at click
        self.assertTrue(feedback_pg.check_feedback_navigation())
        self.assertEqual(feedback_pg.get_feeedback_search_placeholder_value(), "Search by keyword")
        self.assertNotEqual(feedback_pg.message_count,0)
        
        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_feedback_chart))



    """
    Litmus 13597 - input:Verify the layout of right hand section containing statistics data
    Litmus 13716 - input:Verify while visiting section
    """

    def test_the_right_panel_layout(self):

        feedback_pg = feedback_page.FeedbackPage(self.selenium)
        feedback_pg.go_to_feedback_page()

        self.assertEqual(feedback_pg.get_message_total_header(), "Messages")
        self.assertNotEqual(feedback_pg.get_message_total_count, 0)

        self.assertEqual(feedback_pg.mentioned_filter.mentioned_header, "Often Mentioned Toggle")
        self.assertNotEqual(feedback_pg.mentioned_filter.mentioned_count, 0)

        self.assertEqual(feedback_pg.visiting_filter.visiting_header , "While Visiting Toggle")
        self.assertNotEqual(feedback_pg.visiting_filter.visiting_count, 0)



    """
    Litmus 13598 - input:Verify the layout of footer area
    """

    def test_the_footer_area_layout(self):
        feedback_pg = feedback_page.FeedbackPage(self.selenium)
        feedback_pg.go_to_feedback_page()

        #TODO: check css background for image
        #self.selenium.get_text("css=#funnel")

        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_footer_creative_cmmons_attribution_share_alike_license))
        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_footer_legal_notices))
        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_footer_noted))
        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_footer_privacy_policy))
        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_footer_report_trademark_abuse))

        self.assertTrue(feedback_pg.is_element_visible(feedback_pg.get_footer_language_dropdown))


if __name__ == "__main__":
    unittest.main()
