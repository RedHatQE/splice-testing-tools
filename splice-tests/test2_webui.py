import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_2(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest, Splice_has_WebUI):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test2")
        # creating orgs
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("satellite-1", self.ss.config["manifest"])
        for step in range(84):
            splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_active_first_week(self):
        """
        Active report first week
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=15, days_end=8, current=1, state=['Active'])

    def test_02_inactive_first_week(self):
        """
        Inactive report first week
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=15, days_end=8, state=['Inactive'])

    def test_03_consolidated_first_week(self):
        """
        Consolidated report first week
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=15, days_end=8, current=1, state=['Active', 'Inactive'])

    def test_04_active_second_week(self):
        """
        Active report second week
        Expecting 1 invalid subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=7, days_end=1, invalid=1, state=['Active'])

    def test_05_inactive_second_week(self):
        """
        Inactive report second week
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=7, days_end=1, state=['Inactive'])

    def test_06_consolidated_second_week(self):
        """
        Consolidated report second week
        Expecting 1 invalid subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=7, days_end=1, invalid=1, state=['Active', 'Inactive'])

    def test_07_active_both_weeks(self):
        """
        Active report both weeks
        Expecting 1 invalid subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=15, days_end=1, invalid=1, state=['Active'])

    def test_08_inactive_both_week(self):
        """
        Inactive report both weeks
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=15, days_end=1, state=['Inactive'])

    def test_09_consolidated_both_weeks(self):
        """
        Consolidated report both weeks
        Expecting 1 invalid subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=15, days_end=1, invalid=1, state=['Active', 'Inactive'])

    def test_10_active_history(self):
        """
        Active report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Active'])

    def test_11_inactive_history(self):
        """
        Inactive report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Inactive'])

    def test_12_consolidated_history(self):
        """
        Consolidated report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Active', 'Inactive'])

    def test_13_active_future(self):
        """
        Active report future month
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Active'])

    def test_14_inactive_future(self):
        """
        Inactive report future month
        Expecting 1 invalid subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Inactive'], invalid=1)

    def test_15_consolidated_future(self):
        """
        Consolidated report future month
        Expecting 1 invalid subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Active', 'Inactive'], invalid=1)

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello, full_reset=True)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
