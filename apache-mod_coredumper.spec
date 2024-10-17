#Module-Specific definitions
%define mod_name mod_coredumper
%define mod_conf A35_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	20
License:	Apache License
Group:		System/Servers
URL:		https://www.outoforder.cc/projects/apache/mod_coredumper/
Source0: 	http://www.outoforder.cc/downloads/mod_coredumper/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		mod_coredumper-0.1.0-modname.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	coredumper-devel
Epoch:		1

%description
mod_coredumper uses the CoreDumper library from Google to fetch a
GDB compatible core file from Apache, over HTTP.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

perl -pi -e "s|APR_FOPEN_READ|APR_READ|g" src/mod_coredumper.c

%build
%{_bindir}/apxs -lcoredumper -I%{_includedir}/google -c src/mod_coredumper.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc LICENSE NOTICE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-18mdv2012.0
+ Revision: 772610
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-17
+ Revision: 678296
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-16mdv2011.0
+ Revision: 587954
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-15mdv2010.1
+ Revision: 516082
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-14mdv2010.0
+ Revision: 406566
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-13mdv2009.1
+ Revision: 325681
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-12mdv2009.0
+ Revision: 234884
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-11mdv2009.0
+ Revision: 215561
- fix rebuild

* Mon May 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-10mdv2009.0
+ Revision: 206227
- rebuild
- rebuild

* Sat Mar 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-8mdv2008.1
+ Revision: 182264
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.1.0-7mdv2008.1
+ Revision: 170714
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-6mdv2008.0
+ Revision: 82549
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-5mdv2008.0
+ Revision: 65632
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2007.1
+ Revision: 140660
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-3mdv2007.1
+ Revision: 79394
- Import apache-mod_coredumper

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-3mdv2007.0
- rebuild

* Wed Dec 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.1.0-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.1.0-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.1.0-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sat Mar 19 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.1.0-1mdk
- initial package

