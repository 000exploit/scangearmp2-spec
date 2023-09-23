%define base_name scangearmp2
%define _arc %(getconf LONG_BIT)
%define CNCP_LIBS_COM libcncpmslld2 libcncpnet2 libcncpnet20 libcncpnet30

Name:           %{base_name}-sane
Version:        4.60.0
Release:        1%{?dist}
Summary:        Canon ScanGear MP v2 scanner utility and sane backend
License:        GPL and custom:canon
URL:            https://github.com/ThierryHFR/scangearmp2
Source0:	https://github.com/ThierryHFR/scangearmp2/releases/download/%{version}/%{base_name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  libjpeg
BuildRequires:  sane-backends-devel
BuildRequires:  intltool
BuildRequires:  gtk3-devel
Requires:	sane-backends

# Define the architecture
%ifarch x86_64
ExclusiveArch:  x86_64
%endif

%description
Canon ScanGear MP v2 scanner utility and sane backend.

%prep
%autosetup -p1 -n %{base_name}

%build
%define builddir %{_builddir}/%{name}-%{version}
mkdir -p %{builddir}
rm -rf %{builddir}
echo "Starting build ..."
cmake -H. -B%{builddir} -DCMAKE_INSTALL_PREFIX=/
make -C%{builddir} -j4

%install
rm -rf %{buildroot}
make -C%{builddir} install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/usr/share/licenses/%{name}/
mv %{buildroot}/usr/share/%{base_name}/doc/* %{buildroot}/usr/share/licenses/%{name}/
rmdir %{buildroot}/usr/share/%{base_name}/doc/

mkdir -p %{buildroot}/.%{_udevrulesdir}
mv %{buildroot}/etc/udev/rules.d/80-canon_mfp2.rules %{buildroot}/.%{_udevrulesdir}
rm -rf %{buildroot}/etc/udev

%files
%license /usr/share/licenses/%{name}/*
%{_bindir}/%{base_name}
%{_datadir}/applications/%{base_name}.desktop
%{_datadir}/locale/*/LC_MESSAGES/%{base_name}.mo
%dir %{_datadir}/%{base_name}
%{_datadir}/%{base_name}/%{base_name}.glade
%{_datadir}/%{base_name}/%{base_name}.glade.h
%dir %{_libdir}/bjlib
%attr(644,root,root) %{_libdir}/bjlib/canon_mfp2.conf
%attr(644,root,root) %{_libdir}/bjlib/canon_mfp2_net.ini
%{_libdir}/libcncpmslld2.so*
%{_libdir}/libcncpnet2.so*
%{_libdir}/libcncpnet20.so*
%{_libdir}/libcncpnet30.so*
%attr(644,root,root) %{_libdir}/sane/libsane-canon_pixma.so*
%config(noreplace) %{_sysconfdir}/canon-scan.xml
%{_sysconfdir}/sane.d/canon_pixma.conf
%{_sysconfdir}/sane.d/dll.d/mfp2
%attr(644,root,root) %{_udevrulesdir}/80-canon_mfp2.rules

%changelog
* Sat Sep 23 2023 000exploit <illialoo99+rpm@gmail.com> - 4.60.0-1
- Initial release
