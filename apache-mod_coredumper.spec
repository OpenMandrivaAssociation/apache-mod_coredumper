#Module-Specific definitions
%define mod_name mod_coredumper
%define mod_conf A35_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	%mkrel 15
License:	Apache License
Group:		System/Servers
URL:		http://www.outoforder.cc/projects/apache/mod_coredumper/
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_coredumper uses the CoreDumper library from Google to fetch a
GDB compatible core file from Apache, over HTTP.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

perl -pi -e "s|APR_FOPEN_READ|APR_READ|g" src/mod_coredumper.c

%build
%{_sbindir}/apxs -lcoredumper -I%{_includedir}/google -c src/mod_coredumper.c

%install
rm -rf %{buildroot}

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
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE NOTICE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
