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
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Dave Hunt <dhunt@mozilla.com>
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

from vars import ConnectionParameters
import unittest
import urllib2
import pytest
xfail = pytest.mark.xfail


class TestRedirects(unittest.TestCase):

    _user_agent_firefox = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    _user_agent_safari = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27'

    def _check_redirect(self, start_url, end_url, user_agent=_user_agent_firefox, locale='en-US'):
        request = urllib2.Request(ConnectionParameters.baseurl + start_url)
        opener = urllib2.build_opener()
        request.add_header('User-Agent', user_agent)
        request.add_header('Accept-Language', locale)
        f = opener.open(request)
        opener.close()
        self.assertEqual(f.url, ConnectionParameters.baseurl + end_url)

    def test_root_without_locale_redirects_to_root_with_german_locale(self):
        self._check_redirect('/', '/de/', locale='de')

    def test_root_without_locale_redirects_to_root_with_locale(self):
        self._check_redirect('/', '/en-US/')

    def test_beta_without_locale_redirects_to_root_with_locale(self):
        self._check_redirect('/beta/', '/en-US/')

    def test_beta_with_locale_redirects_to_root_with_locale(self):
        self._check_redirect('/en-US/beta/', '/en-US/')

    def test_release_without_locale_redirects_to_root_with_locale(self):
        self._check_redirect('/release/', '/en-US/')

    def test_release_with_locale_redirects_to_root_with_locale(self):
        self._check_redirect('/en-US/release/', '/en-US/')

    def test_feedback_search_without_locale_redirects_to_feedback_search_with_locale(self):
        self._check_redirect('/search?sentiment=happy', '/en-US/search?sentiment=happy')

    def test_beta_feedback_search_without_locale_redirects_to_feedback_search_with_locale(self):
        self._check_redirect('/beta/search?sentiment=sad', '/en-US/search?sentiment=sad')

    def test_beta_feedback_search_with_locale_redirects_to_feedback_search_with_locale(self):
        self._check_redirect('/en-US/beta/search?sentiment=idea', '/en-US/search?sentiment=idea')

    def test_release_feedback_search_without_locale_redirects_to_feedback_search_with_locale(self):
        self._check_redirect('/release/search?sentiment=happy', '/en-US/search?sentiment=happy')

    def test_release_feedback_search_with_locale_redirects_to_feedback_search_with_locale(self):
        self._check_redirect('/en-US/release/search?sentiment=sad', '/en-US/search?sentiment=sad')

    def test_themes_without_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/themes/', '/en-US/themes/')

    def test_beta_themes_without_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/beta/themes/', '/en-US/themes/')

    def test_beta_themes_with_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/en-US/beta/themes/', '/en-US/themes/')

    def test_release_themes_without_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/release/themes/', '/en-US/themes/')

    def test_release_themes_with_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/en-US/release/themes/', '/en-US/themes/')

    def test_sites_without_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/sites/', '/en-US/sites/')

    def test_beta_sites_without_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/beta/sites/', '/en-US/sites/')

    def test_beta_sites_with_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/en-US/beta/sites/', '/en-US/sites/')

    def test_release_sites_without_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/release/sites/', '/en-US/sites/')

    def test_release_sites_with_locale_redirects_to_themes_with_locale(self):
        self._check_redirect('/en-US/release/sites/', '/en-US/sites/')

    def test_idea_without_locale_redirects_to_idea_with_locale(self):
        self._check_redirect('/idea/', '/en-US/idea/')

    def test_beta_idea_without_locale_redirects_to_idea_with_locale(self):
        self._check_redirect('/beta/idea/', '/en-US/idea/')

    def test_beta_idea_with_locale_redirects_to_idea_with_locale(self):
        self._check_redirect('/en-US/beta/idea/', '/en-US/idea/')

    def test_release_idea_without_locale_redirects_to_idea_with_locale(self):
        self._check_redirect('/release/idea/', '/en-US/idea/')

    def test_release_idea_with_locale_redirects_to_idea_with_locale(self):
        self._check_redirect('/en-US/release/idea/', '/en-US/idea/')

    def test_happy_without_locale_redirects_to_happy_with_locale(self):
        self._check_redirect('/happy/', '/en-US/happy/')

    def test_beta_happy_without_locale_redirects_to_happy_with_locale(self):
        self._check_redirect('/beta/happy/', '/en-US/happy/')

    def test_beta_happy_with_locale_redirects_to_happy_with_locale(self):
        self._check_redirect('/en-US/beta/happy/', '/en-US/happy/')

    def test_release_happy_without_locale_redirects_to_happy_with_locale(self):
        self._check_redirect('/release/happy/', '/en-US/happy/')

    def test_release_happy_with_locale_redirects_to_happy_with_locale(self):
        self._check_redirect('/en-US/release/happy/', '/en-US/happy/')

    def test_sad_without_locale_redirects_to_sad_with_locale(self):
        self._check_redirect('/sad/', '/en-US/sad/')

    def test_beta_sad_without_locale_redirects_to_sad_with_locale(self):
        self._check_redirect('/beta/sad/', '/en-US/sad/')

    def test_beta_sad_with_locale_redirects_to_sad_with_locale(self):
        self._check_redirect('/en-US/beta/sad/', '/en-US/sad/')

    def test_release_sad_without_locale_redirects_to_sad_with_locale(self):
        self._check_redirect('/release/sad/', '/en-US/sad/')

    def test_release_sad_with_locale_redirects_to_sad_with_locale(self):
        self._check_redirect('/en-US/release/sad/', '/en-US/sad/')

    def test_feedback_without_locale_redirects_to_feedback_with_locale(self):
        self._check_redirect('/feedback/', '/en-US/feedback/')

    def test_beta_feedback_without_locale_redirects_to_feedback_with_locale(self):
        self._check_redirect('/beta/feedback/', '/en-US/feedback/')

    def test_beta_feedback_with_locale_redirects_to_feedback_with_locale(self):
        self._check_redirect('/en-US/beta/feedback/', '/en-US/feedback/')

    def test_release_feedback_without_locale_redirects_to_feedback_with_locale(self):
        self._check_redirect('/release/feedback/', '/en-US/feedback/')

    def test_release_feedback_with_locale_redirects_to_feedback_with_locale(self):
        self._check_redirect('/en-US/release/feedback/', '/en-US/feedback/')

    def test_sad_redirects_to_download_when_not_using_firefox(self):
        self._check_redirect('/sad/', '/en-US/download', user_agent=self._user_agent_safari)

    def test_happy_redirects_to_download_when_not_using_firefox(self):
        self._check_redirect('/happy/', '/en-US/download', user_agent=self._user_agent_safari)

    def test_idea_redirects_to_download_when_not_using_firefox(self):
        self._check_redirect('/idea/', '/en-US/download', user_agent=self._user_agent_safari)

    def test_feedback_redirects_to_download_when_not_using_firefox(self):
        self._check_redirect('/feedback/', '/en-US/download', user_agent=self._user_agent_safari)

if __name__ == "__main__":
    unittest.main()
