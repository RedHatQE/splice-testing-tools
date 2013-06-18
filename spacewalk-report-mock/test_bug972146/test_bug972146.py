import os
import sys
import datetime
import yaml

path = os.path.dirname(sys.argv[0])

sys.path.append(path + "/../")

from common import *

fd_users = open('%s/template_users.yaml' % path, 'r')
users = yaml.safe_load(fd_users.read())
fd_users.close()


def generate(dirname):
    print_all("%s/step1" % dirname, {'host_guests': [],
                                     'cloned_channels': [],
                                     'users': [users],
                                     'splice_export': []})
    users['organization'] = 'TestOrg2'
    print_all("%s/step2" % dirname, {'host_guests': [],
                                     'cloned_channels': [],
                                     'users': [users],
                                     'splice_export': []})

if len(sys.argv) > 1:
    generate(sys.argv[1])
else:
    generate("./")
