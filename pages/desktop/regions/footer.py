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
#   Bebe <florin.strugariu@softvision.ro>
#   Dave Hunt <dhunt@mozilla.com>
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

from page import Page


class Footer(Page):

    _privacy_policy_link_locator = "css=#footer-links > a:nth(0)"
    _legal_notices_link_locator = "css=#footer-links > a:nth(1)"
    _report_trademark_abuse_link_locator = "css=#footer-links > a:nth(2)"
    _about_input_link_locator = "css=#footer-links > a:nth(3)"
    _unless_otherwise_noted_link_locator = "css=#copyright > p:nth(1) > a:nth(0)"
    _creative_commons_link_locator = "css=#copyright > p:nth(1) > a:nth(1)"
    _language_dropdown_locator = "id=language"

    @property
    def is_language_dropdown_visible(self):
        return self.selenium.is_visible(self._language_dropdown_locator)

    @property
    def privacy_policy(self):
        return self.selenium.get_text(self._privacy_policy_link_locator)

    @property
    def legal_notices(self):
        return self.selenium.get_text(self._legal_notices_link_locator)

    @property
    def report_trademark_abuse(self):
        return self.selenium.get_text(self._report_trademark_abuse_link_locator)

    @property
    def unless_otherwise_noted(self):
        return self.selenium.get_text(self._unless_otherwise_noted_link_locator)

    @property
    def creative_commons(self):
        return self.selenium.get_text(self._creative_commons_link_locator)

    @property
    def about_input(self):
        return self.selenium.get_text(self._about_input_link_locator)
