import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_bug972942(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])
        splicetestlib.fake_spacewalk_test(self.ss.Instances["FAKE_SPACEWALK"][0], "test_sat_nosockinfo")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def _test(self):
        uuid = self.katello.list_systems('satellite-1')[0]['uuid']
        sockets = self.katello.show_system("1e73b493-67bf-4f17-999e-bdcd41b4bf67")['facts']['cpu.cpu_socket(s)']
        nose.tools.assert_equals(socket, "1")

    def _cleanup(self):
        pass

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
