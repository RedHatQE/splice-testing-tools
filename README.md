Splice testing tools
====================

Overview
--------
Splice (https://github.com/Splice/) is enhanced reporting engine for Katello (https://github.com/katello). splice-testing-tools is a framework for testing it.

What is being tested
--------------------
Splice contains 2 parts: spacewalk-splice-tool (SST) and reporting UI.

The workflow is:
* Get data from Spacewalk by running spacewalk-report over ssh (4 reports are being used: users, splice-export, host-guests, and cloned-channels). This is performed once in 4 hours is real life.
* Create similar picture in Katello
* Get data from Katello and put it into historical Mongo database. This is performed once in 10 minutes is real life.
* Reporting UI displays reports based on resulting historical Mongo database.

Splice testing tools consist of 3 parts:
* spacewalk-report-mock tool to simulate any historical data sequence (so-called 'steps' - a sequence of reports from spacewalk). Testing is performed without real Spacewalk server.
* normal tests
* UI tests

How to run testing
------------------
WARNING: some tests (\*\_deleted\_\*) rewind date back in time. SSL certs created in future won't work. To make everything work rewind date on your system BEFORE installing katello packages, e.g. 'date -s "2013-01-01 00:00:00"'

- Create empty Katello setup
- Install 'Splice': yum -y install spacewalk-splice-tool splice ruby193-rubygem-splice_reports
- Allow external connections for ports 80, 443, and 8088
- Do katello-configure
- Create swreport user and configure passwordless ssh for splice user. Example:

         useradd -m swreport
         su - swreport -c 'mkdir -p $HOME/.ssh'
         echo "command=\"spacewalk-report \\\"\$SSH_ORIGINAL_COMMAND\\\"\"" `cat /var/lib/splice/.ssh/id_rsa.pub` >> /home/swreport/.ssh/authorized_keys
         chown swreport.swreport /home/swreport/.ssh/authorized_keys
         chmod 700 /home/swreport/.ssh
         chmod 600 /home/swreport/.ssh/authorized_keys
         restorecon /home/swreport/.ssh/authorized_keys
         cat > /var/lib/splice/.ssh/config <<EOF
         Host localhost
            StrictHostKeyChecking no
            UserKnownHostsFile=/dev/null
         Host `hostname`
            StrictHostKeyChecking no
            UserKnownHostsFile=/dev/null
         EOF
         chown splice.splice /var/lib/splice/.ssh/config
         sed -i 's,^ssh_key_path=.*$,ssh_key_path=/var/lib/splice/.ssh/id_rsa,' /etc/splice/checkin.conf

- Disable cron jobs (to avoid collision with test runs)

         sed -i 's,^[^#],#&,' /etc/cron.d/{splice-sst-sync,spacewalk-sst-sync}
         service crond reload

- Build 'spacewalk-report-mock' package from this repo ('tito build --rpm --test') and install it on the host (only 'spacewalk-report-mock' package needs to be installed)

- If you rewinded date before installing Katello it's time to change it back.

- Prepare manifest for testing. It should contain several 'RHEL' subscriptions only!

Create splice-testing.yaml, example:

     Config: {manifest: /home/user/manifest.zip, katello_user: admin, katello_password: admin, katello_deployment: sam}
     Instances:
     - {private_hostname: ec2-1-2-3-4.eu-west-1.compute.amazonaws.com, public_hostname: ec2-1-2-3-4.eu-west-1.compute.amazonaws.com,
       role: KATELLO, username: root, key_filename: /home/user/.pem/eu-west-1-iam.pem}
     - {private_hostname: ec2-1-2-3-4.eu-west-1.compute.amazonaws.com, public_hostname: ec2-1-2-3-4.eu-west-1.compute.amazonaws.com,
       role: FAKE_SPACEWALK, username: root, key_filename: /home/user/.pem/eu-west-1-iam.pem}

Both roles (KATELLO, FAKE_SPACEWALK) are required! Put this file in the top directory of this repo.

You can run any test now. Example:

     % nosetests -vv splice-tests/test1.py
     nose.config: INFO: Ignoring files matching ['^\\.', '^_', '^setup\\.py$']
     test1.test_splice_1.test_00_setup ... ok
     Active report last week ... ok
     Inactive report last week ... ok
     Consolidated report last week ... ok
     Active report next week ... ok
     Inactive report next week ... ok
     Consolidated report next week ... ok
     Active report last 24h ... ok
     Inactive report last 24h ... ok
     Consolidated report last 24h ... ok
     test1.test_splice_1.test_99_cleanup ... ok
     
     ----------------------------------------------------------------------
     Ran 11 tests in 580.514s
     
     OK

WARNING: \*\_deleted\_\* tests take long (e.g. 2 hours) to finish.

Internals
---------
Each test contains 2 parts:
- Data generator in spacewalk-report-mock package on Katello side (spacewalk-report-mock/ directory)
- Actual test code

Data generator does the following:
- Takes report templates (YAML files)
- Generates 'steps' with data where something changes (checkin times, installed products, system facts,...)

Data generator can be tested manually:

    ## Choosing data sequence
    # spacewalk-report-set test1

    ## Getting reports for first step
    # spacewalk-report users
    organization_id,organization,user_id,username,last_name,first_name,position,email,role,creation_time,last_login_time,active
    1,Testing Org,1,admin,Admin,Admin,,vitty@redhat.com,Organization Administrator;Satellite Administrator,2013-05-24 08:57:50,,enabled
    # spacewalk-report splice-export
    server_id,organization,org_id,name,hostname,ip_address,ipv6_address,registered_by,registration_time,last_checkin_time,software_channel,entitlements,system_group,virtual_host,architecture,hardware,memory,sockets,is_virtualized
    # spacewalk-report host-guests
    server_id,guests
    # spacewalk-report cloned-channels
    original_channel_label,original_channel_name,new_channel_label,new_channel_name

    ## Selecting next step
    # spacewalk-report-set -n

    ## Getting reports for second step
    # spacewalk-report users
    organization_id,organization,user_id,username,last_name,first_name,position,email,role,creation_time,last_login_time,active
    1,Testing Org,1,admin,Admin,Admin,,vitty@redhat.com,Organization Administrator;Satellite Administrator,2013-05-24 08:57:50,,enabled
    # spacewalk-report splice-export
    server_id,organization,org_id,name,hostname,ip_address,ipv6_address,registered_by,registration_time,last_checkin_time,software_channel,entitlements,system_group,virtual_host,architecture,hardware,memory,sockets,is_virtualized
    1000010000,Testing Org,1,ip-10-64-147-151.eu-west-1.compute.internal,ip-10-64-147-151.eu-west-1.compute.internal,10.64.147.151,::1,admin,2013-05-01 00:00:00,2013-10-19 12:50:12,rhel-x86_64-server-6,Spacewalk Management Entitled Servers,,,x86_64,1 CPUs 1 Sockets; eth0 10.64.147.151/255.255.254.0 12:31:43:07:94:69; lo 127.0.0.1/255.0.0.0 00:00:00:00:00:00,1655,1,No
    # spacewalk-report host-guests
    server_id,guests
    # spacewalk-report cloned-channels
    original_channel_label,original_channel_name,new_channel_label,new_channel_name

Data is being generaten when you do 'spacewalk-report-set <test-name>' and cached in '/var/lib/spacewalk-report-mock/' directory. '/var/lib/spacewalk-report-mock/current' link points to current step, 'spacewalk-report-set -n' steps to next step.

Test code uploads data by running SST ('sudo -u splice spacewalk-report') and then checks exported report against expected result, e.g.:

         # ...
         self.splice_check_report(days_start=7, days_end=1, current=1, invalid=1, state=['Active'])
         # that will create 'Active' report starting 7 days ago till 1 day ago (nearly 'last week') and expects one system to be 'current', the other one - 'invalid'.

What gets into reports
----------------------
See doc/REPORTS.md

Contact
-------
vkuznets at redhat.com
