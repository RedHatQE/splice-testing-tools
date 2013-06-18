import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_bug972146(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])
        splicetestlib.fake_spacewalk_test(self.ss.Instances["FAKE_SPACEWALK"][0], "test_bug972146")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def _test(self):
        org_name = ""
        for org in self.katello.list_organizations():
            if org["label"] == 'satellite-1':
                org_name = org["name"]
        nose.tools.assert_equals(org_name, "TestOrg1")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        for org in self.katello.list_organizations():
            if org["label"] == 'satellite-1':
                org_name = org["name"]
        nose.tools.assert_equals(org_name, "TestOrg2")

    def _cleanup(self):
        pass

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
