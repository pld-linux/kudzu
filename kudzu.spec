Summary:	The Red Hat Linux hardware probing tool
Summary(pl):	Narz�dzie do wykrywania sprz�tu
Name:		kudzu
Version:	0.99.89
Release:	0.2
License:	GPL
Group:		Applications/System
URL:		http://rhlinux.redhat.com/kudzu/
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	196e6357ab6acd54ff8f785c10cb2d78
Source1:	%{name}.init
Patch0:		%{name}-nopython.patch
Patch1:		%{name}-gcc295.patch
BuildRequires:	newt-devel
BuildRequires:	pciutils-devel
BuildRequires:	popt-devel
BuildRequires:	python
BuildRequires:	python-devel
PreReq:		modutils >= 2.3.11-5
Requires:	pam >= 0.74-17
Requires:	hwdata
%ifarch ia64
Requires:	/usr/sbin/eepro100-diag
%endif
Obsoletes:	rhs-hwdiag
Obsoletes:	setconsole
Conflicts:	Xconfigurator <= 4.9
Conflicts:	mouseconfig < 4.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kudzu is a hardware probing tool run at system boot time to determine
what hardware has been added or removed from the system.

%description -l pl
Kudzu to narz�dzie do wykrywania sprz�tu uruchamiane przy w��czaniu
systemu, okre�laj�ce jaki sprz�t zosta� dodany lub usuni�ty.

%package devel
Summary:	Development files needed for hardware probing using kudzu
Summary(pl):	Pliki dla programist�w u�ywaj�cych kudzu do wykrywania sprz�tu
Group:		Development/Libraries
Requires:	pciutils-devel

%description devel
The kudzu-devel package contains the libkudzu library, which is used
for hardware probing and configuration.

%description devel -l pl
Ten pakiet zawiera bibliotek� libkudzu, u�ywan� do wykrywania sprz�tu
i konfiguracji.

%package rc
Summary:	rc-scripts for kudzu
Summary(pl):	Skrypty rc dla kudzu
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}

%description rc
rc-scripts for kudzu.

%description rc -l pl
Skrypty rc dla kudzu.

%prep
%setup -q
%patch0 -p1 -b .nopython
%patch1 -p1
install %{SOURCE1} .

# hack: do not start kudzu on s390/s390x on bootup
%ifarch s390 s390x
perl -pi -e "s/345/-/g" kudzu.init
%endif

%build
ln -s `pwd` kudzu

%{__make} all kudzu ktest \
	RPM_OPT_FLAGS="%{rpmcflags} -I." \
	DIET=

%{__make} -C ddcprobe

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install install-program \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install -C ddcprobe \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post rc
/sbin/chkconfig --add kudzu
if [ -f /var/lock/subsys/kudzu ]; then
	/etc/rc.d/init.d/kudzu restart >&2
else
	echo "Run \"/etc/rc.d/init.d/kudzu start\" to start kudzu %{version} services."
fi

%preun rc
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/kudzu ]; then
		/etc/rc.d/init.d/kudzu stop >&2
	fi
	/sbin/chkconfig --del kudzu
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README hwconf-description
%attr(755,root,root) %{_sbindir}/kudzu
%attr(755,root,root) %{_sbindir}/module_upgrade
%attr(755,root,root) %{_sbindir}/updfstab
%attr(755,root,root) %{_sbindir}/ddcprobe
%{_mandir}/man8/*
%{_libdir}/python*/site-packages/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu

%files rc
%defattr(644,root,root,755)
%config(noreplace) %{_sysconfdir}/sysconfig/kudzu
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/kudzu
%config(noreplace) %{_sysconfdir}/updfstab.conf
%config %{_sysconfdir}/updfstab.conf.default
