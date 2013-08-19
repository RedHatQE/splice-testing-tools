Name:		splice-testing-tools
Version:	0.2
Release:	1%{?dist}
Summary:	Splice Testing library

Group:		Development/Tools
License:	GPLv3+
URL:		https://github.com/RedHatQE/splice-testing-tools
Source0:	%{name}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:	python-devel
Requires:	python-nose PyYAML python-selenium-wrapper splice-testing-pageobjects

%description
%{summary}

%package -n spacewalk-report-mock
Summary:	Spacewalk-report mocking tool
Group:		Development/Tools

%description -n spacewalk-report-mock
%{summary}

%if 0%{?with_selenium:1}
%package -n selenium-splice-server
Summary: selenium and Xvfb services
Group: Development/Tools
Requires: xorg-x11-server-Xvfb java

%description -n selenium-splice-server
The Xvfb and selenium services to use when testing splice
%endif

%prep
%setup -q

%build

%install
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/spacewalk-report-mock

%if 0%{?with_selenium:1}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_javadir}/%{name}
cp selenium/selenium-server-standalone-2.31.0.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/selenium-server.jar
%else
rm -f $RPM_BUILD_ROOT%{_unitdir}/selenium-*.service $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/selenium-splice.conf
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n spacewalk-report-mock
%{_bindir}/spacewalk-report-set test1

%if 0%{?with_selenium:1}
%post -n selenium-splice-server
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload &> /dev/null ||:
%endif

%preun -n selenium-splice-server
%if 0%{?fedora} >= 15
/bin/systemctl --no-reload disable selenium-splice.service
/bin/systemctl stop selenium-splice.service
%endif

%postun -n selenium-splice-server
%if 0%{?fedora} >= 15
/bin/systemctl daemon-reload &> /dev/null
if [ "$1" -ge "1" ] ; then
   /bin/systemctl try-restart selenium-splice.service &> /dev/null
fi
%endif
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%attr(0755, root, root) %{_bindir}/*.py
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/splice-testing.yaml
%{python_sitelib}/*.egg-info
%{python_sitelib}/splicetestlib/*.py*
%attr(0644, root, root) %{_datadir}/%name/splice-tests/*.py
%exclude %{_datadir}/%name/splice-tests/*.py?

%files -n spacewalk-report-mock
%attr(0755, root, root) %{_bindir}/spacewalk-report
%attr(0755, root, root) %{_bindir}/spacewalk-report-set
%{_datadir}/%name/spacewalk-report-mock
%exclude %{_datadir}/%name/spacewalk-report-mock/*.py?
%exclude %{_datadir}/%name/spacewalk-report-mock/*/*.py?
%{_sharedstatedir}/spacewalk-report-mock

%if 0%{?with_selenium:1}
%files -n selenium-splice-server
%if 0%{?fedora} >= 15
%config(noreplace) %attr(0640, root, root) %{_unitdir}/selenium-splice-xvfb.service
%config(noreplace) %attr(0640, root, root) %{_unitdir}/selenium-splice.service
%config(noreplace) %attr(0640, root, root) %{_sysconfdir}/sysconfig/selenium-splice.conf
%endif
%attr(0644, root, root) %{_javadir}/%{name}/selenium-server.jar
%endif

%changelog
* Thu Jun 13 2013 Vitaly Kuznetsov <vitty@redhat.com> 0.2-1
- make selenium build optional (vitty@redhat.com)

* Wed Jun 12 2013 Milan Kovacik <mkovacik@redhat.com> 0.1-2
- add selenium-related sub-package

* Wed Jun 05 2013 Vitaly Kuznetsov <vitty@redhat.com> 0.1-1
- new package built with tito

