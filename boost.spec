# To Build:
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# sudo yum -y install bzip2-devel gcc44-c++ python-devel python-libs libicu-devel openmpi-libs
# wget http://downloads.sourceforge.net/project/boost/boost/1.54.0/boost_1_54_0.tar.gz -O ~/rpmbuild/SOURCES/boost_1_54_0.tar.gz
# wget https://raw.github.com/nmilford/rpm-boost/master/boost.spec -O ~/rpmbuild/SPECS/boost.spec
# rpmbuild -bb ~/rpmbuild/SPECS/boost.spec

%define major_ver 1
%define minor_ver 54
%define patch_lvl 0
%define flat_ver  %{major_ver}_%{minor_ver}_%{patch_lvl}
%define dot_ver   %{major_ver}.%{minor_ver}.%{patch_lvl}

Name:           boost
Version:        %{dot_ver}
Release:        1
Summary:        The Boost C++ headers and shared development libraries
Group:          System Environment/Libraries
License:        Boost
URL:            http://www.boost.org/
Source0:        http://downloads.sourceforge.net/project/boost/boost/%{dot_ver}/boost_%{flat_ver}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  bzip2-devel
BuildRequires:  gcc44-c++
BuildRequires:  python-devel
BuildRequires:  python-libs
BuildRequires:  libicu-devel
BuildRequires:  openmpi-libs
Requires:       bzip2
Requires:       python-libs
Provides:       boost-date-time
Provides:       boost-filesystem
Provides:       boost-graph 
Provides:       boost-iostreams
Provides:       boost-program-options
Provides:       boost-python
Provides:       boost-regex
Provides:       boost-serialization
Provides:       boost-signals
Provides:       boost-system
Provides:       boost-test
Provides:       boost-thread
Provides:       boost-wave
Conflicts:      boost141
Conflicts:      boost141-date-time
Conflicts:      boost141-devel
Conflicts:      boost141-doc
Conflicts:      boost141-filesystem
Conflicts:      boost141-graph
Conflicts:      boost141-graph-mpich2
Conflicts:      boost141-graph-openmpi
Conflicts:      boost141-iostreams
Conflicts:      boost141-math
Conflicts:      boost141-mpich2
Conflicts:      boost141-mpich2-devel
Conflicts:      boost141-mpich2-python
Conflicts:      boost141-openmpi
Conflicts:      boost141-openmpi-devel
Conflicts:      boost141-openmpi-python
Conflicts:      boost141-program-options
Conflicts:      boost141-python
Conflicts:      boost141-regex
Conflicts:      boost141-serialization
Conflicts:      boost141-signals
Conflicts:      boost141-signals
Conflicts:      boost141-static
Conflicts:      boost141-system
Conflicts:      boost141-test
Conflicts:      boost141-thread
Conflicts:      boost141-wave   

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been proposed for inclusion in the C++
Standards Committee's upcoming C++ Standard Library Technical Report.)

%package devel
Summary: The Boost C++ headers and shared development libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Headers and shared object symlinks for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
Static Boost C++ libraries.

%prep
%setup -q -n boost_%{flat_ver}

%build
BOOST_ROOT=`pwd`
export BOOST_ROOT
./bootstrap.sh --prefix=%{buildroot}/usr/ --with-toolset=gcc --with-icu

%install
install -d -m 755 %{buildroot}/usr/

# Make sure we're building with GCC 4.4
sed -i -e 's|using gcc|using gcc : : g++44|' %{_builddir}/boost_%{flat_ver}/project-config.jam

./b2 --layout=system install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
/usr/lib/*.so*

%files devel
%defattr(-, root, root, -)
%{_includedir}/boost
/usr/lib/*.so*

%files static
%defattr(-, root, root, -)
/usr/lib/*.a

%changelog
* Thu Jul 04 2013 Nathan Milford <nathan@milford.io> 1.54.0-1
- Initial spec.
