Name:		splice-testing-tools
Version:	0.0
Release:	1%{?dist}
Summary:	Splice Testing library

Group:		Development/Python
License:	GPLv3+
URL:		https://github.com/RedHatQE/splice-testing-tools
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:	python-devel

%description

%prep
%setup -q

%build

%install
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT/%{_datadir}/%name/testing-data
ln -s test001 current
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%attr(0755, root, root) %{_bindir}/*
%{_datadir}/%name/testing-data
%{python_sitelib}/*.egg-info
%{python_sitelib}/splicetestlib/*.py*

%changelog
