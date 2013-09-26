import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_rhel4_arches(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_rhel4_arches")
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("satellite-1", self.ss.config["manifest"])
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_products_and_arches(self):
        """
        Checking arches and RHEL product
        """
        systems = self.katello.list_systems('satellite-1')
        assert len(systems) == 4, 'Expecting 4 systems in setup'

        for sys in systems:
            info = self.katello.show_system(sys['uuid'])
            nose.tools.assert_equals(info['installedProducts'][0]['productId'], '69')
            if sys['name'] == 'host1':
                nose.tools.assert_equals(info['facts']['uname.machine'], 'x86_64')
                nose.tools.assert_equals(info['facts']['lscpu.architecture'], 'x86_64')
            elif sys['name'] == 'host4':
                nose.tools.assert_equals(info['facts']['uname.machine'], 'i386')
                nose.tools.assert_equals(info['facts']['lscpu.architecture'], 'i386')
            else:
                nose.tools.assert_equals(info['facts']['uname.machine'], 'ppc64')
                nose.tools.assert_equals(info['facts']['lscpu.architecture'], 'ppc64')

    def test_02_active_week(self):
        """
        Active report last week
        Expecting 2 current and 2 invalid subscription
        """
        self.splice_check_report(days_start=7, days_end=-11, current=2, invalid=2, state=['Active'])

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello, full_reset=False)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
