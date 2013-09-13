import splicetestlib
from splicetestlib.splice_testcase import *
from splicetestlib.splice_testcase_web import *
import nose


class test_splice_deleted_2(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest, Splice_has_WebUI):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_deleted_2")
        # creating orgs
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("satellite-1", self.ss.config["manifest"])
        for step in range(24):
            splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        self.ss.Instances["KATELLO"][0].recv_exit_status("ntpdate pool.ntp.org", timeout=60)

    def test_01_system_was_removed(self):
        """
        Checking if system is not present in Katello
        """
        systems = self.katello.list_systems("satellite-1")
        nose.tools.assert_equals(len(systems), 0)

    def test_02_active_first_two_days(self):
        """
        Active report first two days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=3, current=1, state=['Active'])

    def test_03_inactive_first_two_days(self):
        """
        Inactive report first two days
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=3, state=['Inactive'])

    def test_04_deleted_first_two_days(self):
        """
        Deleted report first two days
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=3, state=['Deleted'])

    def test_05_consolidated_first_two_days(self):
        """
        Consolidated report first two days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=3, current=1, state=['Active', 'Inactive', 'Deleted'])

    def test_06_active_last_two_days(self):
        """
        Active report last two days
        Expecting 0 subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=1, days_end=0, state=['Active'])

    def test_07_inactive_last_two_days(self):
        """
        Inactive report last two days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=1, days_end=0, current=1, state=['Inactive'])

    def test_08_deleted_last_two_days(self):
        """
        Deleted report last two days
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=1, days_end=0, state=['Deleted'])

    def test_09_consolidated_last_two_days(self):
        """
        Consolidated report last two days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=1, days_end=0, current=1, state=['Active', 'Inactive', 'Deleted'])

    def test_10_active_four_days(self):
        """
        Active report four days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=0, current=1, state=['Active'])

    def test_11_inactive_four_days(self):
        """
        Inactive report four days
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=0, state=['Inactive'])

    def test_12_deleted_four_days(self):
        """
        Deleted report four days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=-1, current=1, state=['Deleted'])

    def test_13_consolidated_four_days(self):
        """
        Consolidated report four days
        Expecting 1 current subscription
        """
        Splice_has_WebUI.splice_check_report(days_start=4, days_end=-1, current=1, state=['Active', 'Inactive', 'Deleted'])

    def test_14_active_history(self):
        """
        Active report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Active'])

    def test_15_inactive_history(self):
        """
        Inactive report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Inactive'])

    def test_16_deleted_history(self):
        """
        Deleted report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Deleted'])

    def test_17_consolidated_history(self):
        """
        Consolidated report month ago
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=31, days_end=21, state=['Active', 'Inactive', 'Deleted'])

    def test_18_active_future(self):
        """
        Active report future month
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Active'])

    def test_19_inactive_future(self):
        """
        Inactive report future month
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Inactive'])

    def test_20_deleted_future(self):
        """
        Deleted report future month
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Deleted'])

    def test_21_consolidated_future(self):
        """
        Consolidated report future month
        Expecting 0 subscriptions
        """
        Splice_has_WebUI.splice_check_report(days_start=-21, days_end=-31, state=['Active', 'Inactive', 'Deleted'])

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello, full_reset=True)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
