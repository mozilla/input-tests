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
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
#                 Bob Silverberg <bob.silverberg@gmail.com>
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

Created on Dec 22, 2010

'''

import time

import pytest
xfail = pytest.mark.xfail
from unittestzero import Assert

import submit_idea_page
import thanks_page
import feedback_page


class TestSubmitIdea:

    def test_submitting_idea(self, testsetup):
        """

        This testcase covers # 15104 in Litmus
        1. Verifies the thank you page is loaded

        """
        submit_idea_pg = submit_idea_page.SubmitIdeaPage(testsetup)

        submit_idea_pg.go_to_submit_idea_page()
        idea = 'Automated idea %s' % str(time.time()).split('.')[0]
        submit_idea_pg.set_feedback(idea)
        thanks_pg = submit_idea_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

    def test_submitting_idea_with_unicode_characters(self, testsetup):
        """

        This testcase covers # 15061 in Litmus
        1. Verifies the thank you page is loaded
        
        """
        submit_idea_pg = submit_idea_page.SubmitIdeaPage(testsetup)

        submit_idea_pg.go_to_submit_idea_page()
        idea = u'Automated idea with unicode \u2603 %s' % str(time.time()).split('.')[0]
        submit_idea_pg.set_feedback(idea)
        thanks_pg = submit_idea_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

    @xfail(reason="Bug 655738 - Character count on feedback forms is gone.")
    def test_remaining_character_count(self, testsetup):
        """

        This testcase covers # 15029 in Litmus
        1. Verifies the remaining character count decreases
        2. Verifies that the remaining character count style changes at certain thresholds
        3. Verified that the 'Submit Feedback' button is disabled when character limit is exceeded

        """
        submit_idea_pg = submit_idea_page.SubmitIdeaPage(testsetup)

        submit_idea_pg.go_to_submit_idea_page()
        Assert.equal(submit_idea_pg.remaining_character_count, "250")
        Assert.false(submit_idea_pg.is_remaining_character_count_low)
        Assert.false(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.true(submit_idea_pg.is_submit_feedback_enabled)

        submit_idea_pg.set_feedback("a" * 199)
        Assert.equal(submit_idea_pg.remaining_character_count, "51")
        Assert.false(submit_idea_pg.is_remaining_character_count_low)
        Assert.false(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.true(submit_idea_pg.is_submit_feedback_enabled)

        submit_idea_pg.set_feedback("b")
        Assert.equal(submit_idea_pg.remaining_character_count, "50")
        Assert.true(submit_idea_pg.is_remaining_character_count_low)
        Assert.false(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.true(submit_idea_pg.is_submit_feedback_enabled)

        submit_idea_pg.set_feedback("c" * 24)
        Assert.equal(submit_idea_pg.remaining_character_count, "26")
        Assert.true(submit_idea_pg.is_remaining_character_count_low)
        Assert.false(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.true(submit_idea_pg.is_submit_feedback_enabled)

        submit_idea_pg.set_feedback("d")
        Assert.equal(submit_idea_pg.remaining_character_count, "25")
        Assert.false(submit_idea_pg.is_remaining_character_count_low)
        Assert.true(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.true(submit_idea_pg.is_submit_feedback_enabled)

        submit_idea_pg.set_feedback("e" * 25)
        Assert.equal(submit_idea_pg.remaining_character_count, "0")
        Assert.false(submit_idea_pg.is_remaining_character_count_low)
        Assert.true(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.true(submit_idea_pg.is_submit_feedback_enabled)

        submit_idea_pg.set_feedback("f")
        Assert.equal(submit_idea_pg.remaining_character_count, "-1")
        Assert.false(submit_idea_pg.is_remaining_character_count_low)
        Assert.true(submit_idea_pg.is_remaining_character_count_very_low)
        Assert.false(submit_idea_pg.is_submit_feedback_enabled)


    def test_submitting_same_idea_twice_generates_error_message(self, testsetup):
        """

        This testcase covers # 15119 in Litmus
        1. Verifies feedback submission fails if the same feedback is submitted within a 5 minute window.

        """
        idea = 'Automated idea %s' % str(time.time()).split('.')[0]
        submit_idea_pg = submit_idea_page.SubmitIdeaPage(testsetup)

        submit_idea_pg.go_to_submit_idea_page()
        submit_idea_pg.set_feedback(idea)
        thanks_pg = submit_idea_pg.submit_feedback()
        Assert.true(thanks_pg.is_the_current_page)

        submit_idea_pg.go_to_submit_idea_page()
        submit_idea_pg.set_feedback(idea)
        submit_idea_pg.submit_feedback(expected_result='failure')
        Assert.equal(submit_idea_pg.error_message, 'We already got your feedback! Thanks.')
