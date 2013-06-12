Name:		splice-testing-tools
Version:	0.1
Release:	1%{?dist}
Summary:	Splice Testing library

Group:		Development/Python
License:	GPLv3+
URL:		https://github.com/RedHatQE/splice-testing-tools
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:	python-devel
Requires:	python-nose PyYAML

%description
%{summary}

%package -n spacewalk-report-mock
Summary:	Spacewalk-report mocking tool
Group:		Development/Tools

%description -n spacewalk-report-mock
%{summary}

%package selenium-splice-server
Summary: selenium and Xvfb services
Group: Development/Python
Requires: xorg-x11-server-Xvfb java
%description selenium-splice-server
The Xvfb and selenium services to use when testing splice


%prep
%setup -q

%build

%install
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT/%{_datadir}/%name/spacewalk-report-mock
ln -s test001 current
popd

%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadir}/%{name}
%{__urlhelpercmd} http://selenium.googlecode.com/files/selenium-server-standalone-2.31.0.jar -o $RPM_BUILD_ROOT%{_javadir}/%{name}/selenium-server.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/*.egg-info
%{python_sitelib}/splicetestlib/*.py*

%files -n spacewalk-report-mock
%attr(0755, root, root) %{_bindir}/spacewalk-report
%{_datadir}/%name/spacewalk-report-mock

%files selenium-splice-server
%if 0%{?fedora} >= 15
%config(noreplace) %attr(0640, root, root) %{_unitdir}/selenium-splice-xvfb.service
%config(noreplace) %attr(0640, root, root) %{_unitdir}/selenium-splice.service
%config(noreplace) %attr(0640, root, root) %{_sysconfdir}/sysconfig/selenium-splice.conf
%endif
%attr(0644, root, root) %{_javadir}/%{name}/selenium-server.jar

%post selenium-splice-server
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload &> /dev/null ||:
%endif

%preun selenium-splice-server
%if 0%{?fedora} >= 15
/bin/systemctl --no-reload disable selenium-splice.service
/bin/systemctl stop selenium-splice.service
%endif

%postun selenium-splice-server
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload &> /dev/null
if [ "$1" -ge "1" ] ; then
   /bin/systemctl try-restart selenium-splice.service &> /dev/null
fi
%endif


%changelog
* Wed Jun 12 2013 Milan Kovacik <mkovacik@redhat.com> 0.1-2
- add selenium-related sub-package
* Wed Jun 05 2013 Vitaly Kuznetsov <vitty@redhat.com> 0.1-1
- new package built with tito

