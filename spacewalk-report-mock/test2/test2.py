import os
import sys
import datetime
import yaml

path = os.path.dirname(sys.argv[0])

sys.path.append(path + "/../")

from common import *

fd_splice_export = open('%s/template_splice_export.yaml' % path, 'r')
splice_export = yaml.safe_load(fd_splice_export.read())
fd_splice_export.close()

fd_users = open('%s/template_users.yaml' % path, 'r')
users = yaml.safe_load(fd_users.read())
fd_users.close()


def generate(dirname):
    initial_date = datetime.datetime.now() - datetime.timedelta(0, 84 * 4 * 3600)
    for i in range(1, 42):
        print_all("%s/step%i" % (dirname, i), {'host_guests': [],
                                               'cloned_channels': [],
                                               'users': [users],
                                               'splice_export': [splice_export]})
        splice_export['last_checkin_time'] = (initial_date + datetime.timedelta(0, i * 4 * 3600)).strftime("%Y-%m-%d %H:%M:%S")
    splice_export['software_channel'] = 'rhel-x86_64-hpc-node-6'
    for i in range(42, 85):
        print_all("%s/step%i" % (dirname, i), {'host_guests': [],
                                               'cloned_channels': [],
                                               'users': [users],
                                               'splice_export': [splice_export]})
        splice_export['last_checkin_time'] = (initial_date + datetime.timedelta(0, i * 4 * 3600)).strftime("%Y-%m-%d %H:%M:%S")

if len(sys.argv) > 1:
    generate(sys.argv[1])
else:
    generate("./")
