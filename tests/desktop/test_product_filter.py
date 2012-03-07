#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from unittestzero import Assert
import pytest

from pages.desktop.feedback import FeedbackPage
from pages.desktop.sites import SitesPage


class TestProductFilter:

    @pytest.mark.nondestructive
    def test_feedback_can_be_filtered_by_firefox_versions(self, mozwebqa):
        """This testcase covers # 13602 & 13603 in Litmus.

        1. Verify that at least three firefox versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL

        """
        feedback_pg = FeedbackPage(mozwebqa)

        product = "firefox"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        versions = feedback_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.greater(len(versions), 3)
        for version in [versions[2], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            feedback_pg.product_filter.select_version(version)
            Assert.equal(feedback_pg.product_filter.selected_product, product)
            Assert.equal(feedback_pg.product_filter.selected_version, version)
            Assert.equal(feedback_pg.product_from_url, product)
            Assert.equal(feedback_pg.version_from_url, version)

    @pytest.mark.nondestructive
    def test_feedback_can_be_displayed_for_all_firefox_versions(self, mozwebqa):
        """This testcase covers # 15149 in Litmus.

        1. Verify that filtering by all versions returns results
        2. Verify that the state of the filters are correct after being applied
        3. Verify product and version values in the URL

        """
        feedback_pg = FeedbackPage(mozwebqa)
        # We can't select the all (default) so set to 1st item first then back to default
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_version(1)

        product = "firefox"
        version = "--"
        feedback_pg.product_filter.select_product(product)
        feedback_pg.product_filter.select_version(version)
        Assert.equal(feedback_pg.product_filter.selected_product, product)
        Assert.equal(feedback_pg.product_filter.selected_version, version)
        Assert.equal(feedback_pg.product_from_url, product)
        Assert.equal(feedback_pg.version_from_url, version)

    @pytest.mark.nondestructive
    def test_feedback_can_be_filtered_by_mobile_versions(self, mozwebqa):
        """This testcase covers # 13602 & 13604 in Litmus.

        1. Verify that at least three mobile versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL

        """
        feedback_pg = FeedbackPage(mozwebqa)

        product = "mobile"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        versions = feedback_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.greater(len(versions), 3)
        for version in [versions[2], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            feedback_pg.product_filter.select_version(version)
            Assert.equal(feedback_pg.product_filter.selected_product, product)
            Assert.equal(feedback_pg.product_filter.selected_version, version)
            Assert.equal(feedback_pg.product_from_url, product)
            Assert.equal(feedback_pg.version_from_url, version)

    @pytest.mark.nondestructive
    def test_feedback_can_be_displayed_for_all_mobile_versions(self, mozwebqa):
        """This testcase covers # 15377 in Litmus.

        1. Verify that filtering by all versions returns results
        2. Verify that the state of the filters are correct after being applied
        3. Verify product and version values in the URL

        """
        feedback_pg = FeedbackPage(mozwebqa)

        product = "mobile"
        version = "--"
        feedback_pg.go_to_feedback_page()
        feedback_pg.product_filter.select_product(product)
        feedback_pg.product_filter.select_version(version)
        Assert.equal(feedback_pg.product_filter.selected_product, product)
        Assert.equal(feedback_pg.product_filter.selected_version, version)
        Assert.equal(feedback_pg.product_from_url, product)
        Assert.equal(feedback_pg.version_from_url, version)

    @pytest.mark.nondestructive
    def test_sites_can_be_filtered_by_firefox_versions(self, mozwebqa):
        """This testcase covers # 15043 & 15045 in Litmus.

        1. Verify that at least three firefox versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL

        """
        sites_pg = SitesPage(mozwebqa)

        product = "firefox"
        sites_pg.go_to_sites_page()
        sites_pg.product_filter.select_product(product)
        versions = sites_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.greater(len(versions), 2)
        for version in [versions[1], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            sites_pg.product_filter.select_version(version)
            Assert.equal(sites_pg.product_filter.selected_product, product)
            Assert.equal(sites_pg.product_filter.selected_version, version)
            Assert.equal(sites_pg.product_from_url, product)
            Assert.equal(sites_pg.version_from_url, version)

    @pytest.mark.xfail(Reason='Bug 716854 - Unable to select mobile product from Sites page')
    @pytest.mark.nondestructive
    def test_sites_can_be_filtered_by_mobile_versions(self, mozwebqa):
        """This testcase covers # 15043 & 15044 in Litmus.

        1. Verify that at least three mobile versions exist
        2. Verify that filtering by version returns results
        3. Verify that the state of the filters are correct after being applied
        4. Verify product and version values in the URL

        """
        sites_pg = SitesPage(mozwebqa)

        product = "mobile"
        sites_pg.go_to_sites_page()
        sites_pg.product_filter.select_product(product)
        versions = sites_pg.product_filter.versions
        [Assert.not_equal(version, "") for version in versions]
        Assert.greater(len(versions), 2)
        for version in [versions[1], versions[-1]]:
            print "Checking %s version '%s'." % (product, version)
            sites_pg.product_filter.select_version(version)
            Assert.equal(sites_pg.product_filter.selected_product, product)
            Assert.equal(sites_pg.product_filter.selected_version, version)
            Assert.equal(sites_pg.product_from_url, product)
            Assert.equal(sites_pg.version_from_url, version)
