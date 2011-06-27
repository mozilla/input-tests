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
'''

Created on June 20, 2011

'''
import submit_feedback_page


class SubmitSadPage(submit_feedback_page.SubmitFeedbackPage):

    _feedback_locator = 'id=sad-description'
    _remaining_character_count_locator = 'css=#sad-description-counter'
    _submit_feedback_locator = 'css=#sad .submit span'
    _error_locator = 'css=#sad .errorlist li'
    _back_locator = 'css=#sad > header > nav > a'

    def go_to_submit_sad_page(self):
        self.selenium.open('/feedback#sad')
        self.is_the_current_page
        self.wait_for_element_visible(self._sad_page_locator)

    @property
    def is_submit_feedback_enabled(self):
        return not self.selenium.is_element_present('css=#sad .submit a.disabled')

    def is_visible(self):
        return self.selenium.is_visible(self._sad_page_locator)
