import os
import patchwork
import logging
from splicetestlib.katello import Katello

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
            typeinstance.katello = Katello(typeinstance.ss.Instances["KATELLO"][0])
        else:
            typeinstance.katello = None
        typelist = [typeinstance]
        for cls in typelist:
            logging.debug("Exploring class " + str(cls))
            logging.debug("Adding base classes: " + str(list(cls.__bases__)) + " to typelist")
            for new_cls in list(cls.__bases__):
                if not new_cls in typelist:
                    logging.debug("Appending " + str(new_cls) + " to classlist")
                    typelist.append(new_cls)
            logging.debug("Checking for 'check' method of " + str(cls))
            if hasattr(cls, "check"):
                logging.debug("Calling 'check' for " + str(cls))
                cls.check(typeinstance.ss)

    @classmethod
    def teardownAll(typeinstance):
        typeinstance.ss.__del__()

    def __init__(self):
        if hasattr(self, "_init"):
            self._init()

    def test_01_setup(self):
        if hasattr(self, "_setup"):
            self._setup()

    def test_02_test(self):
        if hasattr(self, "_test"):
            self._test()

    def test_03_cleanup(self):
        if hasattr(self, "_cleanup"):
            self.ss.reconnect_all()
            self._cleanup()

