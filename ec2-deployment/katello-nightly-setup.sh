#! /bin/bash

# logfile
exec &> /var/log/katello-nightly-setup.log 2>&1

# set up iptables
iptables -I INPUT -p tcp --destination-port 443 -j ACCEPT
service iptables save

# hostname
hostname `curl http://169.254.169.254/latest/meta-data/public-hostname`
sed -i s,HOSTNAME=.*$,HOSTNAME=`hostname`, /etc/sysconfig/network

# repos
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -Uvh http://fedorapeople.org/groups/katello/releases/yum/nightly/RHEL/6/x86_64/katello-repos-latest.rpm

# install katello
yum install -y katello-headpin-all

# splice repo
cat > /etc/yum.repos.d/splice.repo << EOF
[splice]
name=splice_el6_x86_64
baseurl=http://ec2-23-22-86-129.compute-1.amazonaws.com/pub/el6/x86_64/
enabled=1
gpgcheck=0
EOF

# rhsm
yum -y install https://s3.amazonaws.com/rhuiqerpm/subscription-manager-1.8.11-1.el6.x86_64.rpm https://s3.amazonaws.com/rhuiqerpm/python-rhsm-1.8.12-1.el6.x86_64.rpm https://s3.amazonaws.com/rhuiqerpm/subscription-manager-migration-data-2.0.1-1.el6sam.noarch.rpm 

# splice
yum -y install splice spacewalk-splice-tool ruby193-rubygem-splice_reports

# setenforce 0
setenforce 0
sed -i s,SELINUX=enforcing,SELINUX=permissive, /etc/sysconfig/selinux

# configure katello
katello-configure --reset-data=YES --deployment=sam --user-pass=admin

# ensure katello is up and running
katello-service start

# generate ssh key for splice user
su - splice -s /bin/sh -c 'ssh-keygen -t rsa -b 1024 -f ~/.ssh/id_rsa -N ""'

cat /home/ec2-user/.ssh/authorized_keys > /root/.ssh/authorized_keys
echo "command=\"spacewalk-report \\\"\$SSH_ORIGINAL_COMMAND\\\"\"" `cat /var/lib/splice/.ssh/id_rsa.pub` >> /root/.ssh/authorized_keys

cat > /var/lib/splice/.ssh/config <<EOF
Host localhost
   StrictHostKeyChecking no
   UserKnownHostsFile=/dev/null
Host `hostname`
   StrictHostKeyChecking no
   UserKnownHostsFile=/dev/null
EOF

chown splice.splice /var/lib/splice/.ssh/config

# stop crond
service crond stop
