Name:		kudzu
Version:	0.99.64
Release:	0.5
License:	GPL
Summary:	The Red Hat Linux hardware probing tool.
Group:		Applications/System
URL:		http://rhlinux.redhat.com/kudzu/
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.init
Obsoletes:	rhs-hwdiag setconsole
Prereq:		chkconfig, modutils >= 2.3.11-5
Requires:	pam >= 0.74-17, hwdata
%ifarch ia64
Requires:	/usr/sbin/eepro100-diag
%endif
Conflicts:	Xconfigurator <= 4.9
Conflicts:	mouseconfig < 4.18
BuildPrereq:	pciutils-devel python-devel python newt-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kudzu is a hardware probing tool run at system boot time to determine
what hardware has been added or removed from the system.

%package devel
Summary:	Development files needed for hardware probing using kudzu.
Group:		Development/Libraries
Requires:	pciutils-devel

%description devel
The kudzu-devel package contains the libkudzu library, which is used
for hardware probing and configuration.

%prep
%setup -q
install %{SOURCE1} .

# hack: do not start kudzu on s390/s390x on bootup
%ifarch s390 s390x
perl -pi -e "s/345/-/g" kudzu.init
%endif

%build
ln -s `pwd` kudzu

%{__make} RPM_OPT_FLAGS="%{optflags} -I." all kudzu ktest

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install install-program DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add kudzu
if [ -f /var/lock/subsys/kudzu ]; then
	/etc/rc.d/init.d/kudzu restart >&2
else
	echo "Run \"/etc/rc.d/init.d/kudzu start\" to start kudzu %{version} services."
fi

%preun
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
%{_mandir}/man8/*
%config(noreplace) /etc/sysconfig/kudzu
%attr(754,root,root) /etc/rc.d/init.d/kudzu
%config(noreplace) %{_sysconfdir}/updfstab.conf
%config %{_sysconfdir}/updfstab.conf.default
%{_libdir}/python*/site-packages/*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu
