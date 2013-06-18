#! /bin/bash

# logfile
exec &> /var/log/spacewalk-nightly-setup.log 2>&1

# set up iptables
iptables -I INPUT -p tcp --destination-port 443 -j ACCEPT
service iptables save

# hostname
hostname `curl http://169.254.169.254/latest/meta-data/public-hostname`
sed -i s,HOSTNAME=.*$,HOSTNAME=`hostname`, /etc/sysconfig/network

# repos
rpm -Uvh http://yum.spacewalkproject.org/1.9/RHEL/6/x86_64/spacewalk-repo-1.9-1.el6.noarch.rpm
rpm -Uvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm

#nigtly
sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/spacewalk-nightly.repo
sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/spacewalk.repo

cat > /etc/yum.repos.d/jpackage-generic.repo <<EOF
[jpackage-generic]
name=JPackage generic
#baseurl=http://mirrors.dotsrc.org/pub/jpackage/5.0/generic/free/
mirrorlist=http://www.jpackage.org/mirrorlist.php?dist=generic&type=free&release=5.0
enabled=1
gpgcheck=1
gpgkey=http://www.jpackage.org/jpackage.asc
EOF

# install spacewalk
yum -y install spacewalk-setup-postgresql
yum -y install spacewalk-postgresql 
yum -y install spacewalk-reports

# answers
cat > /root/spacewalk_answers <<EOF
admin-email = root@localhost
ssl-set-org = Spacewalk Org
ssl-set-org-unit = spacewalk
ssl-set-city = Brno
ssl-set-state = JMK
ssl-set-country = CZ
ssl-password = spacewalk
ssl-set-email = root@localhost
ssl-config-sslvhost = Y
db-backend = postgresql
enable-tftp = N
EOF

spacewalk-setup --disconnected --answer-file=/root/spacewalk_answers --skip-db-diskspace-check

