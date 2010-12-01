class ConnectionParameters:
    server = "localhost"
    #server = "qa-selenium.mv.mozilla.com"
    port = 4444
    #browser = "Firefox-default-b;en-us;MacOSX6"
    browser = "*firefox"
    baseurl = "http://input.stage.mozilla.com"
    #baseurl = "http://input.mozilla.com"
    mobileurl = "http://m.input.stage.mozilla.com"

    page_load_timeout = 120000