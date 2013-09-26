import splicetestlib
from splicetestlib.splice_testcase import *
import nose
import datetime

class test_splice_threaded_sst(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_threaded_sst")
        # creating orgs
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("satellite-1", self.ss.config["manifest"])

    def test_01_test(self):
        time_start = datetime.datetime.now()
        for step in range(10):
            splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0], timeout=1200)
        time_stop = datetime.datetime.now()

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello, full_reset=False)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
