import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_rhel4_mappings(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_rhel4_mappings")
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_products(self):
        """
        Checking that RHEL product was mapped from rhel4 channel
        """
        uuid = self.katello.list_systems('satellite-1')[0]['uuid']
        nose.tools.assert_equals(self.katello.show_system(uuid)['installedProducts'][0]['productId'], '69')

    def test_02_active_week(self):
        """
        Active report last week
        Expecting 1 invalid subscription
        """
        self.splice_check_report(days_start=7, days_end=-1, invalid=1, state=['Active'])

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello, full_reset=True)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
