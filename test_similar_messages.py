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
# Contributor(s): Tobias Markus <tobbi.bugs@googlemail.com>
#                 Dave Hunt <dhunt@mozilla.com>
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
Created on Jan 26, 2011
'''

from unittestzero import Assert

import sites_page
import themes_page
import theme_page


class TestSimilarMessages:

    def test_similar_messages(self, testsetup):
        """
        This testcase covers # 13807 in Litmus
        """
        sites_pg = sites_page.SitesPage(testsetup)
        themes_pg = themes_page.ThemesPage(testsetup)
        theme_pg = theme_page.ThemePage(testsetup)

        sites_pg.go_to_sites_page()
        sites_pg.product_filter.select_product('firefox')
        sites_pg.product_filter.select_version(2, by='index')

        #store the first site's name and click in
        site = sites_pg.site(1)
        site_name = site.name
        site.click_name()

        #click similar messages and navigate to the second page
        themes_pg.theme(1).click_similar_messages()
        theme_pg.click_next_page()

        Assert.equal(theme_pg.messages_heading, 'Theme')
        Assert.equal(theme_pg.page_from_url, '2')
        Assert.equal(theme_pg.theme_callout, 'Theme for ' + site_name)
        Assert.true(theme_pg.message_count > 0)
        Assert.equal(theme_pg.back_link, u'Back to %s \xbb' % site_name)
        [Assert.true(site_name in message.site) for message in theme_pg.messages]
