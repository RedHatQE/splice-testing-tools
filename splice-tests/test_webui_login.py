import splicetestlib
from splicetestlib.splice_testcase import *
from splicetestlib.pageobjects import SE
from splicetestlib.pageobjects.login import LoginPageObject
from splicetestlib.pageobjects.login import LogoutPageObject
from splicetestlib.pageobjects.login import login_ctx
import nose, os, logging, unittest

class test_splice_webui_login(unittest.TestCase, SpliceTestcase, Splice_has_WebUI):
    sam_user = None
    sam_password = None
    sam_url = None
    def _setup(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.__class__.sam_url = "https://" + self.ss.Instances['SAM'][0].hostname
        self.__class__.sam_user = self.ss.config["katello_user"] 
        self.__class__.sam_password = self.ss.config["katello_password"]
        SE.reset(url=self.sam_url)

    def test_01_webui_login(self):
        lpo = LoginPageObject()
        lpo.username = self.sam_user
        lpo.password = self.sam_password
        lpo.submit()

    def test_02_webui_logout(self):
        lpo = LogoutPageObject()
        lpo.submit()

    def test_03_webui_login_ctx(self):
        with login_ctx(sam_url=self.sam_url, username=self.sam_user, password=self.sam_password):
            # just check that navigating somewhere works
            SE.get(SE.current_url + "/sam/dashboard")

    def _cleanup(self):
        pass
