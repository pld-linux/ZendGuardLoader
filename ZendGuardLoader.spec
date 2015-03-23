# DO NOT MODIFY CONTENTS OF PACKAGE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Guard - PHP code guard
Summary(pl.UTF-8):	Zend Guard - optymalizator kodu PHP
Name:		ZendGuardLoader
Version:	5.5.0
Release:	1
License:	Zend License, distributable only if unmodified and for free (see LICENSE)
Group:		Libraries
Source0:	http://downloads.zend.com/guard/5.5.0/%{name}-php-5.3-linux-glibc23-i386.tar.gz
# Source0-md5:	f53e51ecb59e390be5551ff7cc8576b0
Source1:	http://downloads.zend.com/guard/5.5.0/%{name}-php-5.3-linux-glibc23-x86_64.tar.gz
# Source1-md5:	9408297e9e38d5ce2cca92c619b5ad50
URL:		http://www.zend.com/products/zend_guard
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	tar >= 1:1.15.1
BuildRequires:	php%{?php_suffix}-common >= 4:5.3
BuildRequires:	php%{?php_suffix}-common < 4:5.4
Requires(triggerpostun):	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Guard - PHP code guard.

%description -l pl.UTF-8
Zend Guard - optymalizator kodu PHP.

%package -n php%{?php_suffix}-%{name}
Summary:	Zend Guard for PHP 5.x
Summary(pl.UTF-8):	Zend Guard dla PHP 5.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php%{?php_suffix}-common >= 4:5.3
Requires:	php%{?php_suffix}-common < 4:5.4

%description -n php%{?php_suffix}-%{name}
Zend Guard for PHP 5.x.

%description -n php%{?php_suffix}-%{name} -l pl.UTF-8
Zend Guard dla PHP 5.x.

%prep
%setup -q -c

%ifarch %{ix86}
%{__tar} --strip-components=1 -zxf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -zxf %{SOURCE1}
%endif

cat <<'EOF' > zendguardloader.ini
; ZendGuardLoader user settings.
[Zend]
zend_loader.enable=1
;zend_loader.disable_licensing=0
;zend_loader.obfuscation_level_support=3
;zend_loader.license_path=
EOF

cat <<'EOF' > zendguardloaderpack.ini
; ZendGuardLoader package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_guard.version=%{version}
zend_extension=%{_libdir}/Zend/lib/GuardLoader-%{version}/php-5.3.x/ZendGuardLoader.so
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/php}

for d in php-*; do
	install -D $d/ZendGuardLoader.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/GuardLoader-%{version}/$d/ZendGuardLoader.so
done

ln -s %{_sysconfdir}/php%{?php_suffix} $RPM_BUILD_ROOT%{_libdir}/Zend%{_sysconfdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php%{?php_suffix}/conf.d
install zendguardloader.ini $RPM_BUILD_ROOT%{_sysconfdir}/php%{?php_suffix}/conf.d/zendguardloader.ini
install zendguardloaderpack.ini $RPM_BUILD_ROOT%{_sysconfdir}/php%{?php_suffix}/conf.d/zendguardloader_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun -n php%{?php_suffix}-%{name}
if [ "$1" = "0" ]; then
	%php_webserver_restart
fi

%post -n php%{?php_suffix}-%{name}
# let %{_prefix}/lib/Zend%{_sysconfdir} point to php's config dir. php which installed first wins.
# not sure how critical is existence of this etc link at all.
if [ ! -L %{_libdir}/Zend%{_sysconfdir} ]; then
ln -snf %{_sysconfdir}/php%{?php_suffix} %{_libdir}/Zend%{_sysconfdir}
fi
%php_webserver_restart

#%%post
#if [ "$1" = 1 ]; then
#%%banner -e %{name} <<EOF
#Remember to read %{_docdir}/%{name}-%{version}/LICENSE.gz!
#EOF
#fi

%files
%defattr(644,root,root,755)
%doc README.txt
%dir %{_libdir}/Zend
%dir %{_libdir}/Zend/lib
%dir %{_libdir}/Zend/lib/GuardLoader-%{version}
%dir %{_libdir}/Zend/lib/GuardLoader-%{version}/php-*
%attr(755,root,root) %{_libdir}/Zend/lib/GuardLoader-%{version}/php-*/ZendGuardLoader.so
%ghost %{_libdir}/Zend%{_sysconfdir}

%files -n php%{?php_suffix}-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php%{?php_suffix}/conf.d/zendguardloader.ini
%config %verify(not md5 mtime size) %{_sysconfdir}/php%{?php_suffix}/conf.d/zendguardloader_pack.ini
