Summary:	Hardware probing tool.
Name:		kudzu
Version:	0.99.52
Release:	0.1
Group:		Applications/System
License:	GPL
Source:		%{name}-%{version}.tar.gz
URL:		http://rhlinux.redhat.com/kudzu/
BuildRequires:	pciutils-devel
BuildRequires:	python-devel
BuildRequires:	newt-devel
Prereq:		chkconfig, modutils >= 2.3.11-5, /etc/init.d
Requires:	pam >= 0.74-17, hwdata
%ifarch ia64
Requires:	/usr/sbin/eepro100-diag
%endif
Conflicts:	Xconfigurator <= 4.9
Conflicts:	mouseconfig < 4.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	rhs-hwdiag setconsole

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

# hack: do not start kudzu on s390/s390x on bootup
%ifarch s390 s390x
perl -pi -e "s/345/-/g" kudzu.init
%endif

%build
ln -s `pwd` kudzu

make RPM_OPT_FLAGS="%{optflags} -I. -I/usr/include" all kudzu ktest

%install
rm -rf $RPM_BUILD_ROOT
make install install-program DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add kudzu

%preun
if [ $1 = 0 ]; then
	chkconfig --del kudzu
fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc README hwconf-description
%{_sbindir}/kudzu
%{_sbindir}/module_upgrade
%{_sbindir}/updfstab
%{_mandir}/man8/*
%config(noreplace) /etc/sysconfig/kudzu
%config /etc/rc.d/init.d/kudzu
%config(noreplace) /etc/updfstab.conf
%config /etc/updfstab.conf.default
/usr/lib/python*/site-packages/*

%files devel
%defattr(-,root,root)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu
