#
# Conditional build:
%bcond_with	tests	# unit tests (at least one using network)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	websocket-client
Summary:	WebSocket client for Python
Summary(pl.UTF-8):	Klient Webocket dla Pythona
# keep 0.x here for python2 support
Name:		python-%{module}
Version:	0.59.0
Release:	3
License:	LGPL v2.1+
Group:		Libraries/Python
Source0:	https://files.pythonhosted.org/packages/source/w/websocket-client/%{module}-%{version}.tar.gz
# Source0-md5:	19ccf9abcd151b30975e7b52bfd02760
URL:		https://pypi.org/project/websocket-client/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python >= 1:2.7.10
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PySocks
BuildRequires:	python-backports-ssl_match_hostname
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PySocks
BuildRequires:	python3-six
%endif
%endif
Requires:	python-modules >= 1:2.7.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python websocket-client module is WebSocket client for Python. This
provides the low level APIs for WebSocket. All APIs are the
synchronous functions.

This module supports only hybi-13.

%description -l pl.UTF-8
Moduł Pythona websocket-client to klient WebSocket dla Pythona.
Udostępnia niskopoziomowe API WebSocket. Wszystkie API to funkcje
synchroniczne.

Ten moduł obsługuje tylko hybi-13.

%package -n python3-websocket-client
Summary:	WebSocket client for Python
Summary(pl.UTF-8):	Klient Webocket dla Pythona
Group:		Development/Libraries
Requires:	python3-modules >= 1:3.4

%description -n python3-websocket-client
Python websocket-client module is WebSocket client for Python. This
provides the low level APIs for WebSocket. All APIs are the
synchronous functions.

This module supports only hybi-13.

%description -n python3-websocket-client -l pl.UTF-8
Moduł Pythona websocket-client to klient WebSocket dla Pythona.
Udostępnia niskopoziomowe API WebSocket. Wszystkie API to funkcje
synchroniczne.

Ten moduł obsługuje tylko hybi-13.

%prep
%setup -q -n %{module}-%{version}

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

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{wsdump.py,wsdump-%{py3_ver}}

# remove tests that got installed into the buildroot
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/websocket/tests
%endif

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/{wsdump.py,wsdump-%{py_ver}}

%py_postclean
# remove tests that got installed into the buildroot
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/websocket/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc ChangeLog README.md
%attr(755,root,root) %{_bindir}/wsdump-%{py_ver}
%dir %{py_sitescriptdir}/websocket
%{py_sitescriptdir}/websocket/*.py[co]
%{py_sitescriptdir}/websocket_client-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-websocket-client
%defattr(644,root,root,755)
%doc ChangeLog README.md
%attr(755,root,root) %{_bindir}/wsdump-%{py3_ver}
%dir %{py3_sitescriptdir}/websocket
%{py3_sitescriptdir}/websocket/*.py
%{py3_sitescriptdir}/websocket/__pycache__
%{py3_sitescriptdir}/websocket_client-%{version}-py*.egg-info
%endif
