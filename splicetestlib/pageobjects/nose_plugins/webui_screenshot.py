import logging
import os

from nose.plugins import Plugin
from splicetestlib.pageobjects import SE

log = logging.getLogger(__name__)

class Webui_screenshot(Plugin):
    '''Take Screenshots of each testcase steps in a separate directory'''
    dirname = os.getcwd() + "/" + 'Screenshots'
    enabled = True

    def options(self, parser, env=os.environ):
        #FIXME figure out any custom save options; dir...
        super(Webui_screenshot, self).options(parser, env=env)  

    def screenshots_directory(self, test, failed=False, error=False):
        '''generate proper test case screen shot directory name'''
        fmt_in = (self.dirname, str(test.id()))
        if error:
            return "%s/ERROR_%s" % fmt_in
        if failed:
            return "%s/FAILED_%s" % fmt_in
        return "%s/%s" % fmt_in

    def configure(self, options, conf):
        super(Webui_screenshot, self).configure(options, conf)
        if not self.enabled:
            return

    def begin(self):
        '''enable taking screenshots in the SE webdriver wrapper'''
        SE.screenshots_enabled = True

    def beforeTest(self, test):
        '''set separate screenshot directory for each test case'''
        SE.screenshots_directory = self.screenshots_directory(test) 

    def formatError(self, test, err):
        '''rename the testcase directory to denote the error'''
        os.renames(self.screenshots_directory(test), self.screenshots_directory(test, error=True))

    def formatFailure(self, test, err):
        '''rename the testcase directory to denote the failure'''
        os.renames(self.screenshots_directory(test), self.screenshots_directory(test, failed=True))
