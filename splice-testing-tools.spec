Name:		splice-testing-tools
Version:	0.1
Release:	1%{?dist}
Summary:	Splice Testing library

Group:		Development/Tools
License:	GPLv3+
URL:		https://github.com/RedHatQE/splice-testing-tools
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:	python-devel

%description
%{summary}

%package -n spacewalk-report-mock
Summary:	Spacewalk-report mocking tool
Group:		Development/Tools

%description -n spacewalk-report-mock
%{summary}

%prep
%setup -q

%build

%install
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -n spacewalk-report-mock
%{_bindir}/spacewalk-report-set test1

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/*.egg-info
%{python_sitelib}/splicetestlib/*.py*

%files -n spacewalk-report-mock
%attr(0755, root, root) %{_bindir}/spacewalk-report
%attr(0755, root, root) %{_bindir}/spacewalk-report-set
%{_datadir}/%name/spacewalk-report-mock

%changelog
* Wed Jun 05 2013 Vitaly Kuznetsov <vitty@redhat.com> 0.1-1
- new package built with tito

