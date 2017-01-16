%global pypi_name packaging
%if 0%{?fedora}
%global with_python3 0
%endif

Name:           python-%{pypi_name}
Version:        16.8
Release:        2%{?dist}
Summary:        Core utilities for Python packages

License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
BuildRequires:  python2-pytest
BuildRequires:  python-pretend
BuildRequires:  python2-pyparsing
BuildRequires:  python-six
BuildRequires:  python-sphinx

%if 0%{?with_python3}
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-pretend
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
BuildRequires:  python3-sphinx
%endif

%description
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       pyparsing
Requires:       python-six
%description -n python2-%{pypi_name}
python2-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-pyparsing
Requires:       python3-six
%description -n python3-%{pypi_name}
python3-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.
%endif

%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation
%if 0%{?fedora}
Suggests:       python3-%{pypi_name} = %{version}-%{release}
%endif
%description -n python-%{pypi_name}-doc
Documentation for python-packaging

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
# generate html docs 
sphinx-build-3 docs html
%else
sphinx-build docs html
%endif

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} -m pytest tests/
%if 0%{?with_python3}
%{__python3} -m pytest tests/
%endif

%files -n python2-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python2_sitelib}/%{pypi_name}/
%{python2_sitelib}/%{pypi_name}-%{version}-py%{python2_version}.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE LICENSE.APACHE LICENSE.BSD

%changelog
* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 16.8-2
- Rebuild for Python 3.6

* Wed Nov 02 2016 Lumir Balhar <lbalhar@redhat.com> - 16.8-1
- New upstream version

* Fri Sep 16 2016 Lumir Balhar <lbalhar@redhat.com> - 16.7-1
- Initial package.
