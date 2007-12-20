#Module-Specific definitions
%define mod_name mod_coredumper
%define mod_conf A35_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_coredumper is a DSO module for the apache Web server
Name:		apache-%{mod_name}
Version:	0.1.0
Release:	%mkrel 6
License:	Apache License
Group:		System/Servers
URL:		http://www.outoforder.cc/projects/apache/mod_coredumper/
Source0: 	http://www.outoforder.cc/downloads/mod_coredumper/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		mod_coredumper-0.1.0-modname.diff
#BuildRequires:	autoconf2.5
#BuildRequires:	automake1.7
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

# remove these hacks if using apr/apu 1.x
#perl -pi -e "s|apr-1-config|apr-config|g" m4/apache.m4
#perl -pi -e "s|apu-1-config|apu-config|g" m4/apache.m4
perl -pi -e "s|APR_FOPEN_READ|APR_READ|g" src/mod_coredumper.c

%build
#export WANT_AUTOCONF_2_5=1
#rm -f configure
#libtoolize --force --copy && aclocal-1.7 -I m4 && autoheader && automake-1.7 --add-missing --copy --foreign && autoconf
#
#%%configure2_5x \
#    --with-apxs=%{_sbindir}/apxs
#
#%make

# the commented bloat above can be as easy as:

%{_sbindir}/apxs -lcoredumper -I%{_includedir}/google -c src/mod_coredumper.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 src/.libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE NOTICE README TODO
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
