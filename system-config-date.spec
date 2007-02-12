Summary:	A graphical interface for modifying system date and time
Summary(pl.UTF-8):	Graficzny interfejs do zmiany daty i czasu systemowego
Name:		system-config-date
Version:	1.8.2
Release:	0.1
License:	GPL
Group:		Base
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	04b0e69d7d0c4d9fbffde77dfe62522b
URL:		http://fedora.redhat.com/projects/config-tools/
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	python
#Requires(post):	hicolor-icon-theme
#Requires(postun):	hicolor-icon-theme
#Requires:	chkconfig
#Requires:	htmlview
#Requires:	newt
#Requires:	ntp
#Requires:	pygtk2-libglade
Requires:	python-gnome-canvas
#Requires:	python2
#Requires:	rhpl
#Requires:	usermode >= 1.36
Conflicts:	firstboot <= 1.3.26
ExclusiveOS:	Linux
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

%find_lang %{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/system-config-date
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/system-config-date
%py_postclean %{_datadir}/system-config-date

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
	gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi
%endif

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ntp/ntpservers
%dir %{_datadir}/system-config-date
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/system-config-date/ntp.template
%{_datadir}/system-config-date/*.py[co]
%{_datadir}/system-config-date/*.glade
%{_datadir}/system-config-date/regions
%dir %{_datadir}/system-config-date/pixmaps
%{_datadir}/system-config-date/pixmaps/system-config-date.png
%{_datadir}/system-config-date/pixmaps/map1440.png
%{_mandir}/man8/system-config-date*
%lang(fr) %{_mandir}/fr/man8/system-config-date*
%lang(ja) %{_mandir}/ja/man8/system-config-date*
%{_desktopdir}/system-config-date.desktop
%{_iconsdir}/hicolor/48x48/apps/system-config-date.png
