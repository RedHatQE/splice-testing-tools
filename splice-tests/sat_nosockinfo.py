import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_sat_nosockinfo(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])
        splicetestlib.fake_spacewalk_test(self.ss.Instances["FAKE_SPACEWALK"][0], "test_sat_nosockinfo")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def _test(self):
        uuid = self.katello.list_systems('satellite-1')[0]['uuid']
        sockets = self.katello.show_system(uuid)['facts']['cpu.cpu_socket(s)']
        nose.tools.assert_equals(sockets, "1")

    def _cleanup(self):
        pass

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
