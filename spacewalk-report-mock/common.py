import os

def print_data(signature, data):
    result = ','.join(signature)
    for line in data:
        outline = ''
        for field in signature:
            outline += line[field] + ','
        result += '\n' + outline[:-1]
    result += '\n'
    return result

def print_host_guests(data):
    return print_data(['server_id',
                       'guests'],
                      data)

def print_cloned_channels(data):
    return print_data(['original_channel_label',
                       'original_channel_name',
                       'new_channel_label',
                       'new_channel_name'],
                      data)

def print_users(data):
    return print_data(['organization_id',
                       'organization',
                       'user_id',
                       'username',
                       'last_name',
                       'first_name',
                       'position',
                       'email',
                       'role',
                       'creation_time',
                       'last_login_time',
                       'active'],
                      data)

def print_splice_export(data):
    return print_data(['server_id',
                       'organization',
                       'org_id',
                       'name',
                       'hostname',
                       'ip_address',
                       'ipv6_address',
                       'registered_by',
                       'registration_time',
                       'last_checkin_time',
                       'software_channel',
                       'entitlements',
                       'system_group',
                       'virtual_host',
                       'architecture',
                       'hardware',
                       'memory',
                       'sockets'],
                      data)


def print_all(dirname, data):
    try:
        os.mkdir(dirname)
    except OSError, e:
        pass
    for report in 'host_guests', 'cloned_channels', 'users', 'splice_export':
        fd = open("%s/%s.csv" % (dirname, report.replace("_", "-")), "w")
        fd.write(globals()["print_%s" % report](data[report]))
        fd.close()
    fd = open("%s/%s.csv" % (dirname, "fake-checkin-date"), "w")
    if 'fake_checkin_date' in data:
        fd.write(data['fake_checkin_date'])
    fd.close()
