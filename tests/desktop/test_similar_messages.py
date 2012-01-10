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
#   Tobias Markus <tobbi.bugs@googlemail.com>
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

from unittestzero import Assert
import pytest

from pages.desktop.sites import SitesPage


class TestSimilarMessages:

    @pytest.mark.nondestructive
    def test_similar_messages(self, mozwebqa):
        """This testcase covers # 13807 in Litmus."""
        sites_pg = SitesPage(mozwebqa)

        sites_pg.go_to_sites_page()
        sites_pg.product_filter.select_product('firefox')
        sites_pg.product_filter.select_version(2)

        #store the first site's name and click it
        site = sites_pg.sites[0]
        site_name = site.name
        themes_pg = site.click_name()

        #click similar messages and navigate to the second page
        theme_pg = themes_pg.themes[0].click_similar_messages()
        theme_pg.click_next_page()

        Assert.equal(theme_pg.messages_heading, 'THEME')
        Assert.equal(theme_pg.page_from_url, '2')
        Assert.equal(theme_pg.theme_callout, 'Theme for %s' % site_name.lower())
        Assert.greater(len(theme_pg.messages), 0)
        Assert.equal(theme_pg.back_link, u'Back to %s \xbb' % site_name.lower())
        [Assert.contains(site_name.lower(), message.site) for message in theme_pg.messages]
