import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_bug972942(SpliceTestcase, Splice_has_FAKE_SPACEWALK):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_bug972942")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_orgname(self):
        org_name = ""
        for org in self.katello.list_organizations():
            if org["label"] == 'satellite-2':
                org_name = org["name"]
        nose.tools.assert_equals(org_name, "TestOrg1")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        for org in self.katello.list_organizations():
            if org["label"] == 'satellite-2':
                org_name = org["name"]
        nose.tools.assert_equals(org_name, "TestOrg2")

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
