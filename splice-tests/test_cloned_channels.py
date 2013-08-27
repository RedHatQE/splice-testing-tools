import splicetestlib
from splicetestlib.splice_testcase import *
import datetime
import nose

class test_splice_cloned_channels(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_cloned_channels")
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("satellite-1", self.ss.config["manifest"])
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_active_week(self):
        """
        Active report last week
        Expecting 1 current and 1 invalid subscription
        """
        self.splice_check_report(days_start=7, days_end=1, current=1, invalid=1, state=['Active'])

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
