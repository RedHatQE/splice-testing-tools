import splicetestlib
from splicetestlib.splice_testcase import *
import datetime
import nose

class test_splice_1(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.fake_spacewalk_test(self.ss.Instances["FAKE_SPACEWALK"][0], "test1")
        splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("2", self.ss.config["manifest"])
        for step in range(36):
            splicetestlib.sst_step(self.ss.Instances["FAKE_SPACEWALK"][0])
        SpliceTestcase.last_checkin = self.katello.find_last_checkin()

    def test_01_active_week(self):
        date1 = (SpliceTestcase.last_checkin - datetime.timedelta(7)).strftime("%m/%d/%Y")
        date2 = (SpliceTestcase.last_checkin - datetime.timedelta(1)).strftime("%m/%d/%Y")
        # Active report 1 week
        id_rep = self.katello.create_report("test1_rep1", start_date=date1, end_date=date2)
        csv, metadata, expjson = self.katello.run_report(id_rep)
        res_rep = splicetestlib.util.parse_report_json(expjson)
        nose.tools.assert_equal(res_rep["number_of_current"], 1)
        nose.tools.assert_equal(res_rep["number_of_invalid"], 1)
        nose.tools.assert_equal(res_rep["number_of_insufficient"], 0)
        self.katello.delete_report(id_rep)

    def test_02_inactive_week(self):
        date1 = (SpliceTestcase.last_checkin - datetime.timedelta(7)).strftime("%m/%d/%Y")
        date2 = (SpliceTestcase.last_checkin - datetime.timedelta(1)).strftime("%m/%d/%Y")
        # Inctive report 1 week
        id_rep = self.katello.create_report("test1_rep2", start_date=date1, end_date=date2, inactive=True)
        csv, metadata, expjson = self.katello.run_report(id_rep)
        res_rep = splicetestlib.util.parse_report_json(expjson)
        nose.tools.assert_equal(res_rep["number_of_current"], 0)
        nose.tools.assert_equal(res_rep["number_of_invalid"], 0)
        nose.tools.assert_equal(res_rep["number_of_insufficient"], 0)
        self.katello.delete_report(id_rep)

    def test_03_active_next_week(self):
        date1 = (SpliceTestcase.last_checkin + datetime.timedelta(1)).strftime("%m/%d/%Y")
        date2 = (SpliceTestcase.last_checkin + datetime.timedelta(7)).strftime("%m/%d/%Y")
        # Active report next week
        id_rep = self.katello.create_report("test1_rep4", start_date=date1, end_date=date2)
        csv, metadata, expjson = self.katello.run_report(id_rep)
        res_rep = splicetestlib.util.parse_report_json(expjson)
        nose.tools.assert_equal(res_rep["number_of_current"], 0)
        nose.tools.assert_equal(res_rep["number_of_invalid"], 0)
        nose.tools.assert_equal(res_rep["number_of_insufficient"], 0)
        self.katello.delete_report(id_rep)

    def test_04_inactive_next_week(self):
        date1 = (SpliceTestcase.last_checkin + datetime.timedelta(1)).strftime("%m/%d/%Y")
        date2 = (SpliceTestcase.last_checkin + datetime.timedelta(7)).strftime("%m/%d/%Y")
        # Inctive report next week
        id_rep = self.katello.create_report("test1_rep4", start_date=date1, end_date=date2, inactive=True)
        csv, metadata, expjson = self.katello.run_report(id_rep)
        res_rep = splicetestlib.util.parse_report_json(expjson)
        nose.tools.assert_equal(res_rep["number_of_current"], 1)
        nose.tools.assert_equal(res_rep["number_of_invalid"], 1)
        nose.tools.assert_equal(res_rep["number_of_insufficient"], 0)
        self.katello.delete_report(id_rep)

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0])

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
