#!/usr/bin/env python
# -*- coding: utf-8 -*-

# *****BEGIN LICENSE BLOCK *****
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
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#                 Matt Brandt <mbrandt@mozilla.com>
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

import submit_happy_feedback_page
import thanks_page


class TestFeedback:

    def test_submitting_same_feedback_twice(self, testsetup):
        """
        This testcase covers # 15119 in Litmus
        1. Verifies feedback submission fails if the same feedback is submitted within a 5 minute window.
        """
        text = 'I submit this feedback twice within a five minute window and it should fail.'
        submit_happy_feedback_pg = submit_happy_feedback_page.SubmitHappyFeedbackPage(testsetup)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        submit_happy_feedback_pg.set_feedback(text)
        thanks_pg = submit_happy_feedback_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        submit_happy_feedback_pg.set_feedback(text)
        submit_happy_feedback_pg.submit_feedback()
        Assert.equal(submit_happy_feedback_pg.error_message, 'We already got your feedback! Thanks.')

    def test_submitting_feedback_with_unicode_characters(self, testsetup):
        """
        This testcase covers # 15061 in Litmus
        1. Verifies the thank you page is loaded
        """
        submit_happy_feedback_pg = submit_happy_feedback_page.SubmitHappyFeedbackPage(testsetup)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        submit_happy_feedback_pg.set_feedback(u'It made my \u2603 come alive!')
        thanks_pg = submit_happy_feedback_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

    @xfail(reason="Bug 655738 - Character count on feedback forms is gone.")
    def test_remaining_character_count(self, testsetup):
        """
        This testcase covers # 13806 in Litmus
        1. Verifies the remaining character count decreases
        2. Verifies that the remaining character count style changes at certain thresholds
        3. Verified that the 'Submit Feedback' button is disabled when character limit is exceeded
        """
        submit_happy_feedback_pg = submit_happy_feedback_page.SubmitHappyFeedbackPage(testsetup)

        submit_happy_feedback_pg.go_to_submit_happy_feedback_page()
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "140")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.set_feedback("a" * 111)
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "29")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.set_feedback("b")
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "28")
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.set_feedback("c" * 13)
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "15")
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.set_feedback("d")
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "14")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.set_feedback("e" * 14)
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "0")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.true(submit_happy_feedback_pg.is_submit_feedback_enabled)

        submit_happy_feedback_pg.set_feedback("f")
        Assert.equal(submit_happy_feedback_pg.remaining_character_count, "-1")
        Assert.false(submit_happy_feedback_pg.is_remaining_character_count_low)
        Assert.true(submit_happy_feedback_pg.is_remaining_character_count_very_low)
        Assert.false(submit_happy_feedback_pg.is_submit_feedback_enabled)
