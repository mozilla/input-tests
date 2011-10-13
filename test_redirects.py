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

import urllib2
import pytest
from unittestzero import Assert


class TestRedirects:

    _user_agent_firefox = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.5; rv:5.0) Gecko/20100101 Firefox/5.0'
    _user_agent_safari = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'

    def _check_redirect(self, testsetup, start_url, end_url, user_agent=_user_agent_firefox, locale='en-US'):
        if testsetup.selenium:
            testsetup.selenium.open(start_url)
            Assert.equal(testsetup.selenium.get_location(), testsetup.base_url + end_url)
        else:
            request = urllib2.Request(testsetup.base_url + start_url)
            opener = urllib2.build_opener()
            request.add_header('User-Agent', user_agent)
            request.add_header('Accept-Language', locale)
            f = opener.open(request)
            opener.close()
            Assert.equal(f.url, testsetup.base_url + end_url)

    @pytest.mark.skip_selenium
    def test_root_without_locale_redirects_to_root_with_german_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/', '/de/', locale='de')

    @pytest.mark.skip_selenium
    def test_root_without_locale_redirects_to_root_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/', '/en-US/')

    @pytest.mark.skip_selenium
    def test_beta_without_locale_redirects_to_root_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/', '/en-US/')

    @pytest.mark.skip_selenium
    def test_beta_with_locale_redirects_to_root_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/', '/en-US/')

    @pytest.mark.skip_selenium
    def test_release_without_locale_redirects_to_root_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/', '/en-US/')

    @pytest.mark.skip_selenium
    def test_release_with_locale_redirects_to_root_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/', '/en-US/')

    @pytest.mark.skip_selenium
    def test_feedback_search_without_locale_redirects_to_feedback_search_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/?sentiment=happy', '/en-US/?sentiment=happy')

    @pytest.mark.skip_selenium
    def test_beta_feedback_search_without_locale_redirects_to_feedback_search_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/?sentiment=sad', '/en-US/?sentiment=sad')

    @pytest.mark.skip_selenium
    def test_beta_feedback_search_with_locale_redirects_to_feedback_search_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/?sentiment=idea', '/en-US/?sentiment=idea')

    @pytest.mark.skip_selenium
    def test_release_feedback_search_without_locale_redirects_to_feedback_search_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/?sentiment=happy', '/en-US/?sentiment=happy')

    @pytest.mark.skip_selenium
    def test_release_feedback_search_with_locale_redirects_to_feedback_search_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/?sentiment=sad', '/en-US/?sentiment=sad')

    @pytest.mark.skip_selenium
    def test_themes_without_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/themes/', '/en-US/themes/')

    @pytest.mark.skip_selenium
    def test_beta_themes_without_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/themes/', '/en-US/themes/')

    @pytest.mark.skip_selenium
    def test_beta_themes_with_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/themes/', '/en-US/themes/')

    @pytest.mark.skip_selenium
    def test_release_themes_without_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/themes/', '/en-US/themes/')

    @pytest.mark.skip_selenium
    def test_release_themes_with_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/themes/', '/en-US/themes/')

    @pytest.mark.skip_selenium
    def test_sites_without_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/sites/', '/en-US/sites/')

    @pytest.mark.skip_selenium
    def test_beta_sites_without_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/sites/', '/en-US/sites/')

    @pytest.mark.skip_selenium
    def test_beta_sites_with_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/sites/', '/en-US/sites/')

    @pytest.mark.skip_selenium
    def test_release_sites_without_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/sites/', '/en-US/sites/')

    @pytest.mark.skip_selenium
    def test_release_sites_with_locale_redirects_to_themes_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/sites/', '/en-US/sites/')

    def test_idea_without_locale_redirects_to_idea_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/idea/', '/en-US/feedback#idea')

    def test_beta_idea_without_locale_redirects_to_idea_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/idea/', '/en-US/feedback#idea')

    def test_beta_idea_with_locale_redirects_to_idea_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/idea/', '/en-US/feedback#idea')

    def test_release_idea_without_locale_redirects_to_idea_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/idea/', '/en-US/feedback#idea')

    def test_release_idea_with_locale_redirects_to_idea_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/idea/', '/en-US/feedback#idea')

    def test_happy_without_locale_redirects_to_happy_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/happy/', '/en-US/feedback#happy')

    def test_beta_happy_without_locale_redirects_to_happy_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/happy/', '/en-US/feedback#happy')

    def test_beta_happy_with_locale_redirects_to_happy_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/happy/', '/en-US/feedback#happy')

    def test_release_happy_without_locale_redirects_to_happy_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/happy/', '/en-US/feedback#happy')

    def test_release_happy_with_locale_redirects_to_happy_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/happy/', '/en-US/feedback#happy')

    def test_sad_without_locale_redirects_to_sad_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/sad/', '/en-US/feedback#sad')

    def test_beta_sad_without_locale_redirects_to_sad_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/sad/', '/en-US/feedback#sad')

    def test_beta_sad_with_locale_redirects_to_sad_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/sad/', '/en-US/feedback#sad')

    def test_release_sad_without_locale_redirects_to_sad_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/sad/', '/en-US/feedback#sad')

    def test_release_sad_with_locale_redirects_to_sad_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/sad/', '/en-US/feedback#sad')

    @pytest.mark.skip_selenium
    def test_feedback_without_locale_redirects_to_feedback_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/feedback/', '/en-US/feedback/')

    @pytest.mark.skip_selenium
    def test_beta_feedback_without_locale_redirects_to_feedback_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/beta/feedback/', '/en-US/feedback/')

    @pytest.mark.skip_selenium
    def test_beta_feedback_with_locale_redirects_to_feedback_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/beta/feedback/', '/en-US/feedback/')

    @pytest.mark.skip_selenium
    def test_release_feedback_without_locale_redirects_to_feedback_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/release/feedback/', '/en-US/feedback/')

    @pytest.mark.skip_selenium
    def test_release_feedback_with_locale_redirects_to_feedback_with_locale(self, mozwebqa):
        self._check_redirect(mozwebqa, '/en-US/release/feedback/', '/en-US/feedback/')

    @pytest.mark.skip_selenium
    def test_sad_redirects_to_download_when_not_using_firefox(self, mozwebqa):
        self._check_redirect(mozwebqa, '/sad/', '/en-US/download', user_agent=self._user_agent_safari)

    @pytest.mark.skip_selenium
    def test_happy_redirects_to_download_when_not_using_firefox(self, mozwebqa):
        self._check_redirect(mozwebqa, '/happy/', '/en-US/download', user_agent=self._user_agent_safari)

    @pytest.mark.skip_selenium
    def test_idea_redirects_to_download_when_not_using_firefox(self, mozwebqa):
        self._check_redirect(mozwebqa, '/idea/', '/en-US/download', user_agent=self._user_agent_safari)

    @pytest.mark.skip_selenium
    def test_feedback_redirects_to_download_when_not_using_firefox(self, mozwebqa):
        self._check_redirect(mozwebqa, '/feedback/', '/en-US/download', user_agent=self._user_agent_safari)
