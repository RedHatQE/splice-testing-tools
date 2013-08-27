import splicetestlib
from splicetestlib.splice_testcase import *
import datetime
import nose

class test_splice_host_guests(SpliceTestcase, Splice_has_FAKE_SPACEWALK, Splice_has_Manifest):
    def _setup(self):
        splicetestlib.fake_spacewalk_env(self.ss.Instances["FAKE_SPACEWALK"][0], "test_host_guests")
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])
        # uploading manifest
        self.katello.upload_manifest("satellite-1", self.ss.config["manifest"])
        splicetestlib.sst_step(self.ss.Instances["KATELLO"][0], self.ss.Instances["FAKE_SPACEWALK"][0])

    def test_01_host_guests(self):
        """
        Check host guests allocation
        """
        systems = self.katello.list_systems('satellite-1')
        assert len(systems) == 3, 'Expecting 3 systems in setup'
        for sys in systems:
            info = self.katello.show_system(sys['uuid'])
            if sys['name'] in ['ip-10-64-147-152.eu-west-1.compute.internal', 'ip-10-64-147-153.eu-west-1.compute.internal']:
                # guests
                assert 'virt.is_guest' in info['facts'] and info['facts']['virt.is_guest'] == 'true', 'Virt system is not reported as phys'
                assert len(info['guests']) == 0, 'Virt system has guests'
            elif sys['name'] == 'ip-10-64-147-151.eu-west-1.compute.internal':
                # host
                assert len(info['guests']) == 2, 'Host system should have 2 guests'
                assert not 'virt.is_guest' in info['facts'], 'Phys system is not reported as virt'
            else:
                assert False, "Unknown system %s" % sys['name']

    def _cleanup(self):
        splicetestlib.cleanup_katello(self.ss.Instances["KATELLO"][0], self.katello)

if __name__ == "__main__":
    nose.run(defaultTest=__name__, argv=[__file__, '-v'])
