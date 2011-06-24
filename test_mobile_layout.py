import pytest
xfail = pytest.mark.xfail
from unittestzero import Assert

import mobile_feedback_page


class Test_Feedback_Layout:

    def test_the_header_layout(self, testsetup):

        feedback_pg = mobile_feedback_page.FeedbackPage(testsetup)
        feedback_pg.go_to_feedback_page()

        feedback_pg.click_settings()
        Assert.equal(feedback_pg.visible_page, "settings")

        feedback_pg.click_statistics()
        Assert.equal(feedback_pg.visible_page, "statistics")

        feedback_pg.click_feed()
        Assert.equal(feedback_pg.visible_page, "feed")
