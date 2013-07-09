import splicetestlib
from splicetestlib.splice_testcase import *
import nose

class test_splice_3(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test3")
        # creating orgs
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("2", self.ss.config["manifest"])
        for step in range(84):
            splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_active_first_week(self):
        """
        Active report first week
        Expecting 1 current subscription
        """
        self.splice_check_report(days_start=22, days_end=16, current=1)

    def test_02_inactive_first_week(self):
        """
        Inactive report first week
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=22, days_end=16, inactive=True)

    def test_03_active_second_week(self):
        """
        Active report second week
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=13, days_end=8)

    def test_04_inactive_second_week(self):
        """
        Inactive report second week
        Expecting 1 current subscription
        """
        self.splice_check_report(days_start=13, days_end=8, inactive=True, current=1)

    def test_05_active_third_week(self):
        """
        Active report third week
        Expecting 1 invalid subscription
        """
        self.splice_check_report(days_start=7, days_end=1, invalid=1)

    def test_06_inactive_third_week(self):
        """
        Inactive report third week
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=7, days_end=1, inactive=True)

    def test_07_active_all_weeks(self):
        """
        Active report all weeks
        Expecting 1 invalid subscription
        """
        self.splice_check_report(days_start=22, days_end=1, invalid=1)

    def test_08_inactive_all_week(self):
        """
        Inactive report all weeks
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=22, days_end=1, inactive=True)

    def test_09_active_history(self):
        """
        Active report month ago
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=51, days_end=41)

    def test_10_inactive_history(self):
        """
        Inactive report month ago
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=51, days_end=41, inactive=True)

    def test_11_active_future(self):
        """
        Active report future month
        Expecting 0 subscriptions
        """
        self.splice_check_report(days_start=-21, days_end=-31)

    def test_12_inactive_future(self):
        """
        Inactive report future month
        Expecting 1 invalid subscription
        """
        self.splice_check_report(days_start=-21, days_end=-31, inactive=True, invalid=1)

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
