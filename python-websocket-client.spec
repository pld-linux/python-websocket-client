#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	websocket-client
Summary:	WebSocket client for Python
Name:		python-%{module}
Version:	0.35.0
Release:	1
License:	LGPL v2
Group:		Development/Libraries
Source0:	https://pypi.python.org/packages/source/w/websocket-client/websocket_client-%{version}.tar.gz
# Source0-md5:	37015cccff457f841c6f21bae86fa2d0
URL:		https://pypi.python.org/pypi/websocket-client
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python
BuildRequires:	python-setuptools
%{?with_tests:BuildRequires: python-six}
%endif
%if %{with python3}
BuildRequires:	python3
BuildRequires:	python3-setuptools
%endif
Requires:	python-six
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
python-websocket-client module is WebSocket client for Python. This
provides the low level APIs for WebSocket. All APIs are the
synchronous functions.

python-websocket-client supports only hybi-13.

%package -n python3-websocket-client
Summary:	WebSocket client for python
Group:		Development/Libraries
Requires:	python3-six

%description -n python3-websocket-client
python-websocket-client module is WebSocket client for Python. This
provides the low level APIs for WebSocket. All APIs are the
synchronous functions.

python-websocket-client supports only hybi-13.

%prep
%setup -q -n websocket_client-%{version}

%build
%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with python2}
%py_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python3}
%py3_install

mv $RPM_BUILD_ROOT%{_bindir}/{wsdump.py,wsdump-%{py3_ver}}

# unbundle cacert
rm $RPM_BUILD_ROOT%{py3_sitescriptdir}/websocket/cacert.pem
# And link in the mozilla ca
ln -s %{_sysconfdir}/pki/tls/cert.pem $RPM_BUILD_ROOT%{py3_sitescriptdir}/websocket/cacert.pem

# remove tests that got installed into the buildroot
rm -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/websocket/tests
%endif

%if %{with python2}
%py_install
%py_postclean

mv $RPM_BUILD_ROOT%{_bindir}/{wsdump.py,wsdump-%{py_ver}}

# unbundle cacert
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/websocket/cacert.pem
# And link in the mozilla ca
ln -s %{_sysconfdir}/pki/tls/cert.pem $RPM_BUILD_ROOT%{py_sitescriptdir}/websocket/cacert.pem

# remove tests that got installed into the buildroot
rm -r $RPM_BUILD_ROOT%{py_sitescriptdir}/websocket/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{_bindir}/wsdump-%{py_ver}
%dir %{py_sitescriptdir}/websocket
%{py_sitescriptdir}/websocket/*.py[co]
%{py_sitescriptdir}/websocket/cacert.pem
%{py_sitescriptdir}/websocket_client-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-websocket-client
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{_bindir}/wsdump-%{py3_ver}
%dir %{py3_sitescriptdir}/websocket
%{py3_sitescriptdir}/websocket/*.py
%{py3_sitescriptdir}/websocket/__pycache__
%{py3_sitescriptdir}/websocket/cacert.pem
%{py3_sitescriptdir}/websocket_client-%{version}-py*.egg-info
%endif
