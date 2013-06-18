import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_1(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])
        splicetestlib.fake_spacewalk_test(self.ss.Instances["FAKE_SPACEWALK"][0], "test1")
        for step in range(100):
            splicetestlib.fake_spacewalk_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def _test(self):
        pass

    def _cleanup(self):
        pass

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
