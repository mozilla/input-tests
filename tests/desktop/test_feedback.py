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
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla.
#
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Dave Hunt <dhunt@mozilla.com>
#   Matt Brandt <mbrandt@mozilla.com>
#   Bebe <florin.strugariu@softvision.ro>
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


class TestFeedback:

    def test_submitting_same_feedback_twice(self, mozwebqa):
        """This testcase covers # 15119 in Litmus.

        1. Verifies feedback submission fails if the same feedback is submitted within a 5 minute window.

        """
        text = 'I submit this feedback twice within a five minute window and it should fail.'

        from pages.desktop.submit_happy_feedback import SubmitHappyFeedbackPage
        submit_happy_feedback_pg = SubmitHappyFeedbackPage(mozwebqa)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        submit_happy_feedback_pg.type_feedback(text)
        thanks_pg = submit_happy_feedback_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        submit_happy_feedback_pg.type_feedback(text)
        submit_happy_feedback_pg.submit_feedback()
        Assert.equal(submit_happy_feedback_pg.error_message, 'We already got your feedback! Thanks.')

    def test_submitting_feedback_with_unicode_characters(self, mozwebqa):
        """This testcase covers # 15061 in Litmus.

        1. Verifies the thank you page is loaded

        """
        from pages.desktop.submit_happy_feedback import SubmitHappyFeedbackPage
        submit_happy_feedback_pg = SubmitHappyFeedbackPage(mozwebqa)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        submit_happy_feedback_pg.type_feedback(u'It made my \u2603 come alive!')
        thanks_pg = submit_happy_feedback_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

    def test_remaining_character_count(self, mozwebqa):
        """This testcase covers # 13806 in Litmus.

        1. Verifies the remaining character count decreases
        2. Verifies that the remaining character count style changes at certain thresholds
        3. Verified that the 'Submit Feedback' button is disabled when character limit is exceeded

        """
        from pages.desktop.submit_happy_feedback import SubmitHappyFeedbackPage
        submit_happy_feedback_pg = SubmitHappyFeedbackPage(mozwebqa)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "140")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_limited)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_negative)
        Assert.false(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.type_feedback("a" * 111)
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "29")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_limited)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_negative)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.type_feedback("b")
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "28")
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_limited)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_negative)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.type_feedback("c" * 28)
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "0")
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_limited)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_negative)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.type_feedback("d")
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "-1")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_limited)
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_negative)
        Assert.false(submit_happy_feedback_pg.is_submit_feedback_enabled)

    def test_navigating_away_from_initial_submit_feedback_page(self, mozwebqa):
        """Litmus 13651 - Input: Submit feedback page."""
        from pages.desktop.submit_feedback import SubmitFeedbackPage
        submit_feedback_pg = SubmitFeedbackPage(mozwebqa)
        submit_feedback_pg.go_to_submit_feedback_page()

        happy_feedback_pg = submit_feedback_pg.click_happy_feedback()
        Assert.equal(happy_feedback_pg.current_page_url, "%s/en-US/feedback/#happy" % mozwebqa.base_url)
        happy_feedback_pg.click_back()

        sad_feedback_pg = submit_feedback_pg.click_sad_feedback()
        Assert.equal(sad_feedback_pg.current_page_url, "%s/en-US/feedback/#sad" % mozwebqa.base_url)
        sad_feedback_pg.click_back()

        idea_feedback_pg = submit_feedback_pg.click_idea_feedback()
        Assert.equal(idea_feedback_pg.current_page_url, "%s/en-US/feedback/#idea" % mozwebqa.base_url)
        idea_feedback_pg.click_back()

        Assert.equal(submit_feedback_pg.support_page_link_address, 'http://support.mozilla.com/')
