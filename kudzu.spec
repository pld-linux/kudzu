# TODO
# - optflags, cc
Summary:	Hardware probing tool developed by Red Hat
Summary(pl.UTF-8):	Narzędzie do wykrywania sprzętu rozwijane przez Red Hata
Name:		kudzu
Version:	1.2.81
Release:	3
License:	GPL
Group:		Applications/System
# from ftp://download.fedora.redhat.com/pub/fedora/linux/core/development/SRPMS/%{name}-%{version}.src.rpm
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	dfb630c2e4de5813c464869f6d0efd32
Source1:	%{name}.init
Patch0:		%{name}-nopython.patch
URL:		http://fedora.redhat.com/projects/additional-projects/kudzu/
BuildRequires:	gettext-devel
BuildRequires:	pciutils-devel >= 2.2.0-4
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
%pyrequires_eq	python-libs
Requires:	hwdata >= 0.169
Requires:	module-init-tools
Requires:	pam >= 0.75
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

%description -l pl.UTF-8
Kudzu to narzędzie do wykrywania sprzętu uruchamiane przy włączaniu
systemu, określające jaki sprzęt został dodany lub usunięty.

%package devel
Summary:	Development files needed for hardware probing using kudzu
Summary(pl.UTF-8):	Pliki dla programistów używających kudzu do wykrywania sprzętu
Group:		Development/Libraries
Requires:	pciutils-devel

%description devel
The kudzu-devel package contains the libkudzu library, which is used
for hardware probing and configuration.

%description devel -l pl.UTF-8
Ten pakiet zawiera bibliotekę libkudzu, używaną do wykrywania sprzętu
i konfiguracji.

%package rc
Summary:	rc-scripts for kudzu
Summary(pl.UTF-8):	Skrypty rc dla kudzu
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description rc
rc-scripts for kudzu.

%description rc -l pl.UTF-8
Skrypty rc dla kudzu.

%prep
%setup -q
%patch0 -p1 -b .nopython
install %{SOURCE1} .
mv -f po/eu{_ES,}.po
rm -f po/no.po

# hack: do not start kudzu on s390/s390x on bootup
%ifarch s390 s390x
%{__sed} -i "s/345/-/g" kudzu.init
%endif
%{__sed} -i 's/-Wl,-Bstatic -lpopt/-lpopt -Wl,-Bstatic/' Makefile

%build
ln -s `pwd` kudzu

%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags} -I." \
	DIET= \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-program \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=$RPM_BUILD_ROOT%{_libdir}

install fix-mouse-psaux $RPM_BUILD_ROOT%{_sbindir}

for f in $RPM_BUILD_ROOT%{_datadir}/locale/{eu,fi,id,pl,sk,sr,wa}/LC_MESSAGES/kudzu.mo ; do
	[ "`file $f | sed -e 's/.*,//' -e 's/message.*//'`" -le 1 ] && rm -f $f
done
# not supported by glibc (2.7)
rm -fr $RPM_BUILD_ROOT%{_datadir}/locale/ilo
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post rc
/sbin/chkconfig --add kudzu
%service kudzu restart "kudzu %{version} services"

%preun rc
if [ "$1" = "0" ]; then
	%service kudzu stop
	/sbin/chkconfig --del kudzu
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README hwconf-description
%attr(755,root,root) /sbin/kudzu
%attr(755,root,root) %{_sbindir}/kudzu
%attr(755,root,root) %{_sbindir}/fix-mouse-psaux
%{_mandir}/man8/*
%{py_sitedir}/kudzu.py*
%attr(755,root,root) %{py_sitedir}/_kudzumodule.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libkudzu.a
%{_libdir}/libkudzu_loader.a
%{_includedir}/kudzu

%files rc
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/kudzu
%attr(754,root,root) /etc/rc.d/init.d/kudzu
