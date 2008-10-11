Summary:	A graphical interface for modifying system date and time
Summary(pl.UTF-8):	Graficzny interfejs do zmiany daty i czasu systemowego
Name:		system-config-date
Version:	1.9.17
Release:	2
License:	GPL
Group:		Base
# https://fedorahosted.org/releases/s/y/system-config-date/ (not yet)
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	6551690e7362a7d912e3a6a70cba1915
Patch0:		%{name}-desktop.patch
URL:		http://fedoraproject.org/wiki/SystemConfig/date
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	python
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
#Requires:	chkconfig
Requires:	newt
Requires:	ntp-client
#Requires:	pygtk2-libglade
Requires:	python-gnome-canvas
Requires:	python-rhpl
Requires:	python-snack
#Requires:	usermode >= 1.36
Requires:	tzdata
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
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

desktop-file-install --vendor system --delete-original \
	--dir $RPM_BUILD_ROOT%{_desktopdir} \
	--add-category X-Red-Hat-Base \
	$RPM_BUILD_ROOT%{_desktopdir}/system-config-date.desktop

%find_lang %{name} --with-gnome --with-omf

rm $RPM_BUILD_ROOT%{_bindir}/system-config-date
cat > $RPM_BUILD_ROOT%{_bindir}/system-config-date << EOF
#!/bin/sh
/usr/bin/python /usr/share/system-config-date/system-config-date.pyc
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
%doc doc/*
%attr(755,root,root) %{_bindir}/system-config-date
%attr(755,root,root) %{_bindir}/system-config-time
%attr(755,root,root) %{_bindir}/dateconfig
%attr(755,root,root) %{_sbindir}/timeconfig
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/dateconfig
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/system-config-date
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/system-config-time
%config(noreplace) %verify(not md5 mtime size) /etc/security/console.apps/dateconfig
%config(noreplace) %verify(not md5 mtime size) /etc/security/console.apps/system-config-date
%config(noreplace) %verify(not md5 mtime size) /etc/security/console.apps/system-config-time
%dir %{_datadir}/system-config-date
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/system-config-date/ntp.template
%{_datadir}/system-config-date/*.py[co]
%{_datadir}/system-config-date/*.glade
%dir %{_datadir}/system-config-date/pixmaps
%{_datadir}/system-config-date/pixmaps/system-config-date.png
%{_datadir}/system-config-date/pixmaps/map1440.png
%{_mandir}/man8/system-config-date*
%lang(fr) %{_mandir}/fr/man8/system-config-date*
%lang(ja) %{_mandir}/ja/man8/system-config-date*
%{_desktopdir}/system-config-date.desktop
%{_iconsdir}/hicolor/48x48/apps/system-config-date.png
