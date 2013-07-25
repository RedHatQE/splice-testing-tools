import os
import patchwork
import logging
import nose
import datetime
from splicetestlib.katello import Katello
from splicetestlib.util import *

def traverse_mro(type_instance):
    # traverse mro of a type_instance returning a list of type_instances
    # in order from least generic type to most generic type
    # e.g. test_case -> object
    type_list = [type_instance]
    for type_item in type_list:
        type_list += [ type_parent for type_parent in type_item.__bases__ if type_parent not in type_list ]
    return type_list

def call_methods(method_name, object_list, *args, **kvargs):
    # filter + run method based on given method_name on a list of objects
    map(
        lambda object_instance: getattr(object_instance, method_name)(*args, **kvargs),
        filter(
            lambda object_instance: hasattr(object_instance, method_name),
            object_list
        )
    )

class SpliceTestcase(object):
    @classmethod
    def setupAll(typeinstance):
        if "SPLICE_TEST_DEBUG" is os.environ and os.environ["SPLICE_TEST_DEBUG"] != "":
            loglevel = logging.DEBUG
        else:
            loglevel = logging.INFO
        logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        typeinstance.ss = patchwork.Structure()
        if os.path.exists("splice-testing.yaml"):
            typeinstance.ss.setup_from_yamlfile(yamlfile="splice-testing.yaml", output_shell=True)
        else:
            typeinstance.ss.setup_from_yamlfile(yamlfile="/etc/splice-testing.yaml", output_shell=True)
        if "KATELLO" in typeinstance.ss.Instances:
            katello_user = 'admin'
            katello_password = 'admin'
            katello_deployment = 'sam'
            if hasattr(typeinstance.ss, "config"):
                if "katello_user" in typeinstance.ss.config:
                    katello_user = typeinstance.ss.config["katello_user"]
                if "katello_password" in typeinstance.ss.config:
                    katello_password = typeinstance.ss.config["katello_password"]
                if "katello_deployment" in typeinstance.ss.config:
                    katello_deployment = typeinstance.ss.config["katello_deployment"]
            typeinstance.katello = Katello(
                hostname=typeinstance.ss.Instances["KATELLO"][0].hostname,
                username=katello_user,
                password=katello_password,
                deployment=katello_deployment
            )
        else:
            typeinstance.katello = None

        # figure out type-based check-ers and preparators
        typelist = traverse_mro(typeinstance)

        # check from the least generic type up to the most generic type i.e. test_case -> object
        call_methods("check", typelist, typeinstance.ss)

        # call preparers from the most generic type downto the least generic type i.e. object -> test_case
        call_methods("prepare", reversed(typelist), typeinstance.ss)

    @classmethod
    def teardownAll(typeinstance):
        # call cleaners from the least generic type up to the most generic type i.e. test_case -> object
        call_methods("cleanup", traverse_mro(typeinstance), typeinstance.ss)

        # clean-up the ss structure
        typeinstance.ss.__del__()

    def __init__(self):
        if hasattr(self, "_init"):
            self._init()

    def test_00_setup(self):
        if hasattr(self, "_setup"):
            self._setup()

    def test_99_cleanup(self):
        if hasattr(self, "_cleanup"):
            self.ss.reconnect_all()
            self._cleanup()

    @classmethod
    def splice_check_report(typeinstance, days_start=None, days_end=None, past_hours=None, inactive=False, current=0, invalid=0, insufficient=0):
        """
        Create splice report and check it

        @param days_start: Number of past days for report start_date (e.g. 7 means 7 days ago)
        @type days_start: int

        @param days_end: Number of past days for report end_date (e.g. 1 means 1 day ago)
        @type days_end: int

        @param past_hours: Create report for past N hours
        @type past_hours: int

        @param inactive: create Inactive report
        @type inactive: bool

        @param current: expected number of current subscriptions
        @type current: int

        @param invalid: expected number of invalid subscriptions
        @type invalid: int

        @param insufficient: expected number of insufficient subscriptions
        @type insufficient: int
        """
        if not hasattr(typeinstance, "last_checkin") or typeinstance.last_checkin is None:
            typeinstance.last_checkin = typeinstance.katello.find_last_checkin()

        if days_start is not None and days_end is not None:
            date1 = (typeinstance.last_checkin - datetime.timedelta(days_start)).strftime('%m/%d/%Y')
            date2 = (typeinstance.last_checkin - datetime.timedelta(days_end)).strftime('%m/%d/%Y')
            id_rep = typeinstance.katello.create_report('testing_report_%s_%s_%s' % (days_start, days_end, inactive), start_date=date1, end_date=date2, inactive=inactive)
        elif past_hours is not None:
            id_rep = typeinstance.katello.create_report('testing_report_%s_hours_%s' % (past_hours, inactive), time='choose_hour', hours=past_hours, inactive=inactive)
        else:
            # Wrong usage
            assert False
            return
        csv, metadata, expjson = typeinstance.katello.run_report(id_rep)
        res_rep = parse_report_json(expjson)
        nose.tools.assert_equal(res_rep['number_of_current'], current)
        nose.tools.assert_equal(res_rep['number_of_invalid'], invalid)
        nose.tools.assert_equal(res_rep['number_of_insufficient'], insufficient)
        typeinstance.katello.delete_report(id_rep)


class Splice_has_FAKE_SPACEWALK(object):
    _splice_checkin_conf_path = "/etc/splice/checkin.conf"

    @classmethod
    def check(self, ss):
        if (not "FAKE_SPACEWALK" in ss.Instances) or len(ss.Instances["FAKE_SPACEWALK"]) < 1:
            raise nose.exc.SkipTest("can't test without fake spacewalk!")

    @classmethod
    def prepare(self, ss):
        fake_spacewalk = ss.Instances["FAKE_SPACEWALK"][0]
        katello = ss.Instances["KATELLO"][0]

        # back-up the /etc/splice/checkin.conf file
        self._orig_splice_checkin_conf_path = katello.pbm["mktemp"]["--tmpdir=/tmp", "splice_checkin_XXXX.conf"]()
        katello.pbm["cp"]["-f", self._splice_checkin_conf_path, self._orig_splice_checkin_conf_path]()
        
        # set the [spacewalk] section to point to the FAKE_SPACEWALK's SST tool
        import ConfigParser
        katello_conf = ConfigParser.ConfigParser()
        with katello.rpyc.builtins.open(self._splice_checkin_conf_path) as fd:
            katello_conf.readfp(fd)

        katello_conf.set("spacewalk", "host", fake_spacewalk.hostname)
        katello_conf.set("spacewalk", "ssh_key_path", "/var/lib/splice/.ssh/id_rsa")
        if hasattr(ss, "config"):
            if 'katello_deployment' in ss.config:
                katello_conf.set('katello', 'api_url', '/' + ss.config['katello_deployment'])

        with katello.rpyc.builtins.open(self._splice_checkin_conf_path, "w+") as fd:
            katello_conf.write(fd)
        katello.pbm['chown']['root:splice', self._splice_checkin_conf_path]()

    @classmethod
    def cleanup(self, ss):
        # put the original /etc/splice/checkin.conf back
        katello = ss.Instances["KATELLO"][0]
        katello.pbm["mv"]["-f", self._orig_splice_checkin_conf_path, self._splice_checkin_conf_path]()
        del(self._orig_splice_checkin_conf_path)


class Splice_has_Manifest(object):
    @classmethod
    def check(self, ss):
        if (not "manifest" in ss.config):
            raise nose.exc.SkipTest("can't test without manifest!")

class Splice_has_WebUI(object):
    @classmethod
    def check(self, ss):
        if not 'selenium_display' in ss.config:
            raise nose.exc.SkipTest("can't test without selenium_display")

    @classmethod
    def prepare(self, ss):
        self._old_os_environ_display = None
        if 'DISPLAY' in os.environ:
            self._old_os_environ_display = os.environ['DISPLAY']
        os.environ['DISPLAY'] = ss.config['selenium_display']

    @classmethod
    def cleanup(self, ss):
        if self._old_os_environ_display is not None:
            os.environ['DISPLAY'] = self._old_os_environ_display
        else:
            del(os.environ['DISPLAY'])
