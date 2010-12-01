'''
Created on Nov 24, 2010

@author: mozilla
'''

import input_base_page
import vars

import time
import re

page_load_timeout = vars.ConnectionParameters.page_load_timeout

class SitesPage(input_base_page.InputBasePage):
    
    _page_title              =  'Sites'
    _messages_count          =  "css=div[id='big-count'] > p"

        
    
    def __init__(self, selenium):
        '''
            Creates a new instance of the class
        '''
        super(SitesPage,self).__init__(selenium)

    def go_to_sites_page(self):
        self.sel.open('/en-US/sites/')
        count = 0
        while (re.search(self._page_title, self.sel.get_location(), re.IGNORECASE)) is None:
            time.sleep(1)
            count += 1
            if count == 20:
                raise Exception("Sites Page has not loaded")

