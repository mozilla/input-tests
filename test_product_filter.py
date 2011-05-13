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
# Contributor(s): Vishal
#                 David Burns
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
Created on Nov 24, 2010
'''

from unittestzero import Assert

import feedback_page
import sites_page


class TestProductFilter:

    def test_feedback_can_be_filtered_by_firefox_versions(self, testsetup):
        """
        This testcase covers # 13602 & 13603 in Litmus
        1. Verify that at least three firefox versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        product = "firefox"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        versions = feedback_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.true(len(versions) > 3)
        for version in [versions[2], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            feedback_pg.product_filter.select_version(version)
            Assert.equal(feedback_pg.product_filter.selected_product, product)
            Assert.equal(feedback_pg.product_filter.selected_version(), version)
            Assert.equal(feedback_pg.product_from_url, product)
            Assert.equal(feedback_pg.version_from_url, version)

    def test_feedback_can_be_displayed_for_all_firefox_versions(self, testsetup):
        """
        This testcase covers # 15149 in Litmus
        1. Verify that filtering by all versions returns results
        2. Verify that the state of the filters are correct after being applied
        3. Verify product and version values in the URL
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        product = "firefox"
        version = "--"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        feedback_pg.product_filter.select_version(version)
        Assert.equal(feedback_pg.product_filter.selected_product, product)
        Assert.equal(feedback_pg.product_filter.selected_version(), version)
        Assert.equal(feedback_pg.product_from_url, product)
        Assert.equal(feedback_pg.version_from_url, version)

    def test_feedback_can_be_filtered_by_mobile_versions(self, testsetup):
        """
        This testcase covers # 13602 & 13604 in Litmus
        1. Verify that at least three mobile versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        product = "mobile"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        versions = feedback_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.true(len(versions) > 3)
        for version in [versions[2], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            feedback_pg.product_filter.select_version(version)
            Assert.equal(feedback_pg.product_filter.selected_product, product)
            Assert.equal(feedback_pg.product_filter.selected_version(), version)
            Assert.equal(feedback_pg.product_from_url, product)
            Assert.equal(feedback_pg.version_from_url, version)

    def test_feedback_can_be_displayed_for_all_mobile_versions(self, testsetup):
        """
        This testcase covers # 15377 in Litmus
        1. Verify that filtering by all versions returns results
        2. Verify that the state of the filters are correct after being applied
        3. Verify product and version values in the URL
        """
        feedback_pg = feedback_page.FeedbackPage(testsetup)

        product = "mobile"
        version = "--"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        feedback_pg.product_filter.select_version(version)
        Assert.equal(feedback_pg.product_filter.selected_product, product)
        Assert.equal(feedback_pg.product_filter.selected_version(), version)
        Assert.equal(feedback_pg.product_from_url, product)
        Assert.equal(feedback_pg.version_from_url, version)

    def test_sites_can_be_filtered_by_firefox_versions(self, testsetup):
        """
        This testcase covers # 15043 & 15045 in Litmus
        1. Verify that at least three firefox versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL
        """
        sites_pg = sites_page.SitesPage(testsetup)

        product = "firefox"
        sites_pg.go_to_sites_page()
        sites_pg.product_filter.select_product(product)
        versions = sites_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.true(len(versions) > 2)
        for version in [versions[1], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            sites_pg.product_filter.select_version(version)
            Assert.equal(sites_pg.product_filter.selected_product, product)
            Assert.equal(sites_pg.product_filter.selected_version(), version)
            Assert.equal(sites_pg.product_from_url, product)
            Assert.equal(sites_pg.version_from_url, version)

    def test_sites_can_be_filtered_by_mobile_versions(self, testsetup):
        """
        This testcase covers # 15043 & 15044 in Litmus
        1. Verify that at least three mobile versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL
        """
        sites_pg = sites_page.SitesPage(testsetup)

        product = "mobile"
        sites_pg.go_to_sites_page()
        sites_pg.product_filter.select_product(product)
        versions = sites_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.true(len(versions) > 2)
        for version in [versions[1], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            sites_pg.product_filter.select_version(version)
            Assert.equal(sites_pg.product_filter.selected_product, product)
            Assert.equal(sites_pg.product_filter.selected_version(), version)
            Assert.equal(sites_pg.product_from_url, product)
            Assert.equal(sites_pg.version_from_url, version)
