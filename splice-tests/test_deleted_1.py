import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_deleted_1(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_deleted_1")
        # creating orgs
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        for step in range(84):
            splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_system_was_removed(self):
        """
        Checking if system is not present in Katello
        """
        systems = self.katello.list_systems("satellite-1")
        nose.tools.assert_equals(len(systems), 1)

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello.password)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
