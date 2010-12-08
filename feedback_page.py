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
# Portions created by the Initial Developer are Copyright (C) 2___
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
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
Created on Nov 19, 2010
'''

import input_base_page
import vars

import time
import re

page_load_timeout = vars.ConnectionParameters.page_load_timeout


class FeedbackPage(input_base_page.InputBasePage):
    
    _page_title              =  'Welcome'
    _messages_count          =  "css=div[id='big-count'] > p"
    # Matches input.stage.mozilla.com & input.mozilla.com
    _url_regex               =  r'https?://input(\..*)?\.mozilla\.com/en\-US.'

    def __init__(self, selenium):
        """Create a new instance of the class."""
        self.selenium = selenium

    def go_to_feedback_page(self):
        """go to FD page and wait max of until regexp matches the url."""
        self.selenium.open('/')
        current_loc = self.selenium.get_location()
        count = 0
        while not re.search(self._url_regex, current_loc, re.U):
            time.sleep(1)
            count += 1
            if count == 20:
                raise Exception("Home Page has not loaded. Current url is %s" % (current_loc))
