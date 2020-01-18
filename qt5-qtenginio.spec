%global qt_module qtenginio

# define to build docs, need to undef this for bootstrapping
%define docs 1

Summary: Qt5 - Enginio component
Name:    qt5-%{qt_module}
Epoch:   1
Version: 1.6.2
Release: 1%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://doc.qt.io/qt-5/licensing.html
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://www.qt.io
Source0: http://download.qt.io/official_releases/qt/5.6/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel >= 5.6
BuildRequires:  qt5-qtdeclarative-devel

%description
Client library for accessing Enginio service from Qt and QML code.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
License: GFDL
#Requires: %{name} = %{epoch}:%{version}-%{release}
BuildRequires: qt5-qdoc
BuildRequires: qt5-qhelpgenerator
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-opensource-src-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..

make %{?_smp_mflags}

%if 0%{?docs}
# HACK to avoid multilib conflicts in noarch content
# see also https://bugreports.qt.io/browse/QTBUG-42071
QT_HASH_SEED=0; export QT_HASH_SEED
make %{?_smp_mflags} docs
%endif
popd


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot} -C %{_target_platform}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libEng*.prl ; do
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
if [ -f "$(basename ${prl_file} .prl).so" ]; then
rm -fv "$(basename ${prl_file} .prl).la"
sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE* LGPL_EXCEPTION.txt
%{_qt5_libdir}/libEnginio.so.1*
%{_qt5_archdatadir}/qml/Enginio/

%files devel
%{_qt5_headerdir}/Enginio/
%{_qt5_libdir}/libEnginio.so
%{_qt5_libdir}/libEnginio.prl
%dir %{_qt5_libdir}/cmake/Qt5Enginio/
%{_qt5_libdir}/cmake/Qt5Enginio/Qt5EnginioConfig*.cmake
%{_qt5_libdir}/pkgconfig/Enginio.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_enginio*.pri

%if 0%{?docs}
%files doc
%{_qt5_docdir}/qtenginio.qch
%{_qt5_docdir}/qtenginio
%{_qt5_docdir}/qtenginiooverview.qch
%{_qt5_docdir}/qtenginiooverview
%{_qt5_docdir}/qtenginioqml.qch
%{_qt5_docdir}/qtenginioqml
%endif

%if 0%{?_qt5_examplesdir:1}
%files examples
%{_qt5_examplesdir}/
%endif


%changelog
* Wed Jan 11 2017 Jan Grulich <jgrulich@redhat.com> - 1:1.6.2-1
- Update to 1.6.2
  Resolves: bz#1384819

* Tue Aug 30 2016 Jan Grulich <jgrulich@redhat.com> - 1:1.6.1-10
- Increase build version to have newer version than in EPEL
  Resolves: bz#1317402

* Wed Jun 08 2016 Jan Grulich <jgrulich@redhat.com> - 1:1.6.1-1
- Update to 1.6.1
  Resolves: bz#1317402

* Wed Apr 13 2016 Jan Grulich <jgrulich@redhat.com> - 1:1.6.0-5
- Enable documentation
  Resolves: bz#1317402

* Thu Apr 07 2016 Jan Grulich <jgrulich@redhat.com> - 1:1.6.0-4
- Initial version for RHEL
  Resolves: bz#1317402

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:1.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 1:1.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 1.6.0-1
- 1.6.0 final release
- Epoch to adjust the version

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.7.rc
- Update to final RC

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.6
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.5.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.4.beta1
- Fix Release, Fix sources, -docs: fix deps

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.3
- Update to final beta release

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.2
- Official beta release

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.1.rc
- First release
