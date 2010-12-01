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

from page import Page
import vars

import re
import time

page_load_timeout = vars.ConnectionParameters.page_load_timeout

class InputBasePage(Page):

    _app_name_fx              =  "firefox"
    _app_name_mb              =  "mobile"

    _fx_versions              =  ("4.0b1","4.0b2","4.0b3", "4.0b4", "4.0b5", "4.0b6", "4.0b7")
    
    _mb_versions              =  ("1.1", "1.1b1", "4.0b1", "4.0b2")
    
    _product_dropdown         =  "product"
    _version_dropdown         =  "version"
    
    _when_links               =  ("link=1d", "link=7d", "link=30d")

    _feedback_praise_box      =  "praise_bar" 
    _feedback_issues_box      =  "issue_bar" 
    
    _platforms                =  ("os_win7", "os_winxp", "os_mac", "os_vista", "os_linux", "os_")
    
    _locales                  =  {'us' : 'loc_en-US', 
                                  'germany' :'loc_de', 
                                  'spain' :'loc_es',
                                  'russia' :'loc_ru',
                                  'france' :'loc_fr',
                                  'british' :'loc_en-GB',
                                  'poland' :'loc_pl',
                                  'china' :'loc_zh-CN'                                 
                                  }
                  
    _search_results_section    = "messages"
    _search_form               = "kw-search"
    _search_box                = "id_q"

    
    def __init__(self, selenium):
        '''
            Creates a new instance of the class
        '''
        super(InputBasePage,self).__init__(selenium)
            
    def get_default_selected_product(self):
        """
        returns the product selected in the filter by default
        """
        param_val = self._product_dropdown + "@data-selected"
        selected_app = self.selenium.get_attribute(param_val)
        return selected_app
                
    def select_prod_firefox(self):
        """
        selects Firefox from Product filter
        """
        selected_app = self.get_default_selected_product()
        if re.search(self._app_name_fx, selected_app, re.IGNORECASE) is None:
            app_label = "value=%s"%(self._app_name_fx)
            self.selenium.select(self._product_dropdown,app_label)
            self.selenium.wait_for_page_to_load(page_load_timeout)
        
    def select_prod_mobile(self):
        """
        selects Mobile from Product filter
        """
        selected_app = self.get_default_selected_product()
        if re.search(self._app_name_mb, selected_app, re.IGNORECASE) is None:
            app_label = "value=%s" % (self._app_name_mb)
            self.selenium.select(self._product_dropdown,app_label)
            self.selenium.wait_for_page_to_load(page_load_timeout)

    def get_default_selected_version(self):
        """
        returns the version selected in the filter by default
        """
        selected_ver = self.selenium.get_selected_value(self._version_dropdown)
        return selected_ver
          
    def select_firefox_version(self,version):
        """
        selects firefox version,4.0b1
        """
        selected_ver = self.get_default_selected_version()
        if re.search(version, selected_ver, re.IGNORECASE) is None:
            for f_ver in self._fx_versions:
                if re.search(version,f_ver,re.IGNORECASE) is None:
                    continue
                else:
                    ver_label = "value=%s" % (f_ver)
                    self.selenium.select(self._version_dropdown,ver_label)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break
            
        
    def select_mobile_version(self,version):
        """
        selects mobile version,4.0b1
        """
        selected_ver = self.get_default_selected_version()
        if re.search(version, selected_ver, re.IGNORECASE) is None:
            for m_ver in self._mb_versions:
                if re.search(version,m_ver,re.IGNORECASE) is None:
                    continue
                else:
                    ver_label = "value=%s" % (m_ver)
                    self.selenium.select(self._version_dropdown,ver_label)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break
            
    def click_days(self,days):
        """
        clicks 1d/7d/30d
        """
        for time in self._when_links:
            if re.search(days,time,re.IGNORECASE) is None:
                continue
            else:
                if self.selenium.is_checked(time):
                    break
                else:
                    self.selenium.click(time)
                    break

            
    def click_platform(self,os):
        """
        clicks Windows XP/ Android etc.
        """
        for plat in self._platforms:
            if re.search(os,plat,re.IGNORECASE) is None:
                continue
            else:
                if self.selenium.is_checked(plat):
                    break
                else:
                    self.selenium.click(plat)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break
            
    def click_feedback_praise(self):
        """
        clicks Feedback type - Praise
        """
        if self.selenium.is_checked(self._feedback_praise_box):
            pass
        else:
            self.selenium.click(self._feedback_praise_box)
            self.selenium.wait_for_page_to_load(page_load_timeout)
            
    def click_feedback_issues(self):
        """
        clicks Feedback type - Issues
        """
        if self.selenium.is_checked(self._feedback_issues_box):
            pass
        else:
            self.selenium.click(self._feedback_issues_box)
            self.selenium.wait_for_page_to_load(page_load_timeout)
            
    def click_locale(self,country_name):
        """
        clicks US/German/Spanish etc.
        """
        for country,loc_code in self._locales.iteritems():
            if re.search(country_name,country,re.IGNORECASE) is None:
                continue
            else:
                if self.selenium.is_checked(loc_code):
                    break
                else:
                    self.selenium.click(loc_code)
                    self.selenium.wait_for_page_to_load(page_load_timeout)
                    break

    def verify_all_firefox_versions(self):
        """
            checks all Fx versions are present
        """
        for version in self._fx_versions:
            version_locator = "css=select#%s > option[value='%s']" % (self._version_dropdown,version)
            if not (self.selenium.is_element_present(version_locator)):
                raise Exception('Version %s not found in the filter' % (version))
            
    def verify_all_mobile_versions(self):
        """
            checks all mobile versions are present
        """
        for version in self._mb_versions:
            version_locator = "css=select#%s > option[value='%s']" % (self._version_dropdown,version)
            if not (self.selenium.is_element_present(version_locator)):
                raise Exception('Version %s not found in the filter' % (version))
        