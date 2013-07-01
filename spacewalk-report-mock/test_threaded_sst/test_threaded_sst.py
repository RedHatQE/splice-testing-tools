import os
import sys
import datetime
import yaml

path = os.path.dirname(sys.argv[0])

sys.path.append(path + "/../")

from common import *

fd_splice_export = open('%s/template_splice_export.yaml' % path, 'r')
splice_export = []
splice_export.append(yaml.safe_load(fd_splice_export.read()))
fd_splice_export.close()
for i in range(1,300):
    # creating 299 additional systems
    splice_export.append(splice_export[0].copy())
    splice_export[i]['hostname'] += "." + str(i)
    splice_export[i]['name'] += "." + str(i)
    splice_export[i]['server_id']= str(int(splice_export[0]['server_id']) + (10000 * i))
    if i >= 150:
        # changing channel for last 150 systems
        splice_export[i]['software_channel'] = 'rhel-x86_64-server-6'
splice_export[0]['hostname'] += ".0"
splice_export[0]['name'] += ".0"

fd_users = open('%s/template_users.yaml' % path, 'r')
users = yaml.safe_load(fd_users.read())
fd_users.close()


def generate(dirname):
    # 2 weeks back
    initial_date = datetime.datetime.now() - datetime.timedelta(0, 84 * 4 * 3600)
    print_all("%s/step1" % dirname, {'host_guests': [],
                                     'cloned_channels': [],
                                     'users': [users],
                                     'splice_export': []})
    for i in range(1, 85):
        print_all("%s/step%i" % (dirname, i + 1), {'host_guests': [],
                                                   'cloned_channels': [],
                                                   'users': [users],
                                                   'splice_export': splice_export})
        for i in range(300):
            splice_export[i]['last_checkin_time'] = (initial_date + datetime.timedelta(0, i * 4 * 3600)).strftime("%Y-%m-%d %H:%M:%S")

if len(sys.argv) > 1:
    generate(sys.argv[1])
else:
    generate("./")
