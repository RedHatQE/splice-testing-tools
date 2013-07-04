import splicetestlib
from splicetestlib.splice_testcase import *
from splicetestlib.pageobjects import SE
from splicetestlib.pageobjects.login import LoginPageObject
import nose, os, logging, unittest

class test_splice_webui_login(unittest.TestCase, SpliceTestcase, Splice_has_WebUI):
    def _setup(self):
        self.log = logging.getLogger(self.__class__.__name__)
        SE.reset(url="https://" + self.ss.Instances['SAM'][0].hostname)

    def test_01_webui_login(self):
        lpo = LoginPageObject()
        lpo.username = self.ss.config["katello_user"]
        lpo.password = self.ss.config["katello_password"]
        lpo.submit()

    def _cleanup(self):
        pass
