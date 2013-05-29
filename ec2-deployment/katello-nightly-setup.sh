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
yum install -y katello-all

# setenforce 0
setenforce 0
sed -i s,SELINUX=enforcing,SELINUX=permissive, /etc/sysconfig/selinux

# configure katello
katello-configure  --user-pass=pwadmin

# splice repo
cat > /etc/yum.repos.d/splice.repo << EOF
[splice]
name=splice_el6_x86_64
baseurl=http://ec2-23-22-86-129.compute-1.amazonaws.com/pub/el6/x86_64/
enabled=1
gpgcheck=0

[splice-jbeap]
name=splice_jbeap
baseurl=http://ec2-23-22-86-129.compute-1.amazonaws.com/pub/jbeap/el6/
enabled=1
gpgcheck=0
EOF

# splice
yum -y install splice spacewalk-splice-tool ruby193-rubygem-splice_reports

# restart katello
service katello restart
