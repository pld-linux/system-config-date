Summary:	A graphical interface for modifying system date and time
Summary(pl.UTF-8):	Graficzny interfejs do zmiany daty i czasu systemowego
Name:		system-config-date
Version:	1.9.67
Release:	2
License:	GPL
Group:		Base
Source0:	http://fedorahosted.org/released/system-config-date/%{name}-%{version}.tar.bz2
# Source0-md5:	5af4caafb46a9c63a5fcc6e0e6e4d2e4
Patch0:		%{name}-desktop.patch
Patch1:		tzconfig.patch
URL:		http://fedoraproject.org/wiki/SystemConfig/date
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-tools
BuildRequires:	intltool
BuildRequires:	python
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
#Requires:	chkconfig
Requires:	hicolor-icon-theme
Requires:	ntpdate
Requires:	python-gnome-canvas
Requires:	python-pygtk-glade
Requires:	python-slip >= 0.2.11
Requires:	python-snack
Requires:	tzdata
Requires:	usermode-gtk >= 1.94
Conflicts:	firstboot <= 1.3.26
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
system-config-date is a graphical interface for changing the system
date and time, configuring the system time zone, and setting up the
NTP daemon to synchronize the time of the system with a NTP time
server.

%description -l pl.UTF-8
system-config-date to graficzny interfejs do zmiany daty i czasu
systemowego, konfiguracji strefy czasowej i ustawiania demona NTP do
synchronizacji czasu systemowego z serwerem czasu NTP.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor system --delete-original \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_desktopdir}/system-config-date.desktop

%find_lang %{name} --with-gnome --with-omf

rm $RPM_BUILD_ROOT%{_bindir}/system-config-date
cat > $RPM_BUILD_ROOT%{_bindir}/system-config-date << EOF
#!/bin/sh
%{__python} %{_datadir}/system-config-date/system-config-date.pyc
EOF

ln -sf system-config-date $RPM_BUILD_ROOT%{_bindir}/dateconfig
ln -sf system-config-date $RPM_BUILD_ROOT%{_bindir}/system-config-time

%py_comp $RPM_BUILD_ROOT%{_datadir}/system-config-date
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/system-config-date
%py_postclean %{_datadir}/system-config-date

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/system-config-date
%attr(755,root,root) %{_bindir}/system-config-time
%attr(755,root,root) %{_bindir}/dateconfig
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/system-config-date
%config(noreplace) %verify(not md5 mtime size) /etc/security/console.apps/system-config-date
%dir %{_datadir}/system-config-date
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/system-config-date/ntp.conf.template
%{_datadir}/system-config-date/*.py[co]
%{_datadir}/system-config-date/*.glade
%dir %{_datadir}/system-config-date/pixmaps
%{_datadir}/system-config-date/pixmaps/map1440.png
%{_mandir}/man8/system-config-date*
%lang(fr) %{_mandir}/fr/man8/system-config-date*
%lang(ja) %{_mandir}/ja/man8/system-config-date*
%{_desktopdir}/system-config-date.desktop
%{_iconsdir}/hicolor/*/apps/system-config-date.png
%{_iconsdir}/hicolor/*/apps/system-config-date.svg

%dir %{py_sitescriptdir}/scdate
%{py_sitescriptdir}/scdate/*.py[co]
%dir %{py_sitescriptdir}/scdate/core
%{py_sitescriptdir}/scdate/core/*.py[co]
%{py_sitescriptdir}/scdate-%{version}-py*.egg-info
