from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
import logging, os

class SeleniumWrapper(object):
    # a singleton proxy to a default driver instance
    _instance = None
    _direct_attrs = ("_driver",)

    def __new__(cls, *args, **kvargs):
        if not cls._instance:
            cls._instance = super(SeleniumWrapper, cls).__new__(cls, *args, **kvargs)
            # clean-up the singleton at exit --- close the _driver
            import atexit
            atexit.register(cls._instance.__del__)
        return cls._instance

    def __init__(self):
        self._driver = None

    @property
    def driver(self):
        # for special driver use cases
        return self._driver

    @driver.setter
    def driver(self, aDriver):
        # for special driver use cases
        self._driver = aDriver

    def __getattr__(self, attrname):
        # proxy calls to the driver
        if attrname in self.__class__._direct_attrs:
            return self.__dict__[attrname]
        return getattr(self._driver, attrname)

    def __setattr__(self, attrname, value):
        # proxy calls to the driver
        if attrname in self.__class__._direct_attrs:
            self.__dict__[attrname] = value
            return
        setattr(self._driver, attrname, value)

    def __del__(self):
        # close & del the _driver
        try:
            self._driver.close()
        except Exception:
            pass
        del(self._driver)

    def __contains__(self, locator):
        # locator should be a function
        # to examine the driver directly, use SeleniumWrapper().driver instead
        if callable(locator):
            try:
                locator()
                return True
            except NoSuchElementException:
                return False
        else:
            return locator in self._driver

    def reset(self, driver=None, url=None):
        # reset the driver
        # - if driver is None, setup a default one
        # - if url is not None, "get" it
        if self._driver is not None:
            try:
                self._driver.close()
            except Exception as e:
                logging.log(logging.WARNING, "got: %s closing driver" % e)
                
        if driver is None:
            # we'd like to
            # - accept untrusterd certs
            # - automatically save downloads to cwd/Downloads
            profile = FirefoxProfile()
            profile.accept_untrusted_cert = True
            profile.set_preference("browser.download.folderList", 2)
            profile.set_preference("browser.download.dir", os.getcwd() + "/Downloads")
            profile.set_preference("browser.download.manager.showWhenStarting", False)
            profile.set_preference("browser.download.panel.shown", False)
            profile.set_preference("browser.download.show_plugins_in_list", False)
            profile.set_preference("browser.download.closeWhenDone", True)
            profile.set_preference("browser.download.useWindow", False)
            profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
            profile.set_preference(
                "browser.helperApps.neverAsk.saveToDisk",
                ",".join([
                    "application/octet-stream",
                    "application/zip",
                    "application/gzip",
                    "application/bzip2",
                    "application/x-tar"
                ])
            )
            self._driver = Firefox(profile)
        else:
            self._driver = driver

        if url is not None:
            self._driver.get(url)
