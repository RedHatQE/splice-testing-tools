from splicetestlib import SpliceTestcase
import nose

class test_splice_1(SpliceTestcase):
    def _setup(self):
        pass

    def _test(self):
        pass

    def _cleanup(self):
        pass

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
