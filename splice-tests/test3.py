import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_3(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])
        splicetestlib.fake_spacewalk_test(self.ss.Instances["FAKE_SPACEWALK"][0], "test3")
        # creating orgs
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("2", self.ss.config["manifest"])
        for step in range(84):
            splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_test(self):
        pass

    def _cleanup(self):
        pass

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
