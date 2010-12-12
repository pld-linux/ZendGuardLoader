# DO NOT MODIFY CONTENTS OF PACKAGE - AGAINST LICENSE AND MAKES IT UNDISTRIBUTABLE
# AND ALSO IT IS ALREADY STRIPPED.

%define		no_install_post_strip		1
%define		no_install_post_compress_docs	1
%define		no_install_post_chrpath		1
Summary:	Zend Guard - PHP code guard
Summary(pl.UTF-8):	Zend Guard - optymalizator kodu PHP
Name:		ZendGuardLoader
Version:	5.5.0
Release:	0.1
License:	Zend License, distributable only if unmodified and for free (see LICENSE)
Group:		Libraries
Source0:	http://downloads.zend.com/guard/5.5.0/%{name}-php-5.3-linux-glibc23-i386.tar.gz
# Source0-md5:	f53e51ecb59e390be5551ff7cc8576b0
Source1:	http://downloads.zend.com/guard/5.5.0/%{name}-php-5.3-linux-glibc23-x86_64.tar.gz
# Source1-md5:	9408297e9e38d5ce2cca92c619b5ad50
URL:		http://www.zend.com/products/zend_guard
BuildRequires:	rpmbuild(macros) >= 1.344
BuildRequires:	tar >= 1:1.15.1
Requires(triggerpostun):	sed >= 4.0
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Zend Guard - PHP code guard.

%description -l pl.UTF-8
Zend Guard - optymalizator kodu PHP.

%package -n php-%{name}
Summary:	Zend Guard for PHP 5.x
Summary(pl.UTF-8):	Zend Guard dla PHP 5.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	php-common >= 4:5.3

%description -n php-%{name}
Zend Guard for PHP 5.x.

%description -n php-%{name} -l pl.UTF-8
Zend Guard dla PHP 5.x.

%prep
%setup -q -c

%ifarch %{ix86}
%{__tar} --strip-components=1 -zxf %{SOURCE0}
%endif
%ifarch %{x8664}
%{__tar} --strip-components=1 -zxf %{SOURCE1}
%endif

cat <<'EOF' > zendguard.ini
; ZendGuard user settings.
[Zend]
zend_guard.optimization_level=15
EOF

cat <<'EOF' > pack.ini
; ZendGuard package settings. Overwritten with each upgrade.
; if you need to add options, edit %{name}.ini instead
[Zend]
zend_guard.version=%{version}
zend_extension_manager.guard=%{_libdir}/Zend/lib/Guard-%{version}
zend_extension_manager.guard_ts=%{_libdir}/Zend/lib/Guard_TS-%{version}
zend_extension=%{_libdir}/Zend/lib/ZendExtensionManager.so
zend_extension_ts=%{_libdir}/Zend/lib/ZendExtensionManager_TS.so
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/php}

install -D php-*/ZendGuardLoader.so $RPM_BUILD_ROOT%{_libdir}/Zend/lib/Guard-%{version}/php-$d/ZendGuardLoader.so

ln -s %{_sysconfdir}/php $RPM_BUILD_ROOT%{_libdir}/Zend%{_sysconfdir}
ln -s %{_bindir} $RPM_BUILD_ROOT%{_libdir}/Zend/bin

install -d $RPM_BUILD_ROOT%{_sysconfdir}/php/conf.d
install zendguard.ini $RPM_BUILD_ROOT%{_sysconfdir}/php/conf.d/zendguard.ini
install pack.ini $RPM_BUILD_ROOT%{_sysconfdir}/php/conf.d/zendguard_pack.ini

%clean
rm -rf $RPM_BUILD_ROOT

%preun -n php-%{name}
if [ "$1" = "0" ]; then
	%php_webserver_restart
fi

%post -n php-%{name}
# let %{_prefix}/lib/Zend%{_sysconfdir} point to php's config dir. php which installed first wins.
# not sure how critical is existence of this etc link at all.
if [ ! -L %{_libdir}/Zend%{_sysconfdir} ]; then
ln -snf %{_sysconfdir}/php %{_libdir}/Zend%{_sysconfdir}
fi
%php_webserver_restart

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<EOF
Remember to read %{_docdir}/%{name}-%{version}/LICENSE.gz!
EOF
fi

%triggerpostun -- %{name} < 2.5.10a-0.20
if [ -f /etc/php/php.ini ]; then
	cp -f /etc/php/conf.d/ZendGuard.ini{,.rpmnew}
	sed -ne '/^\(zend_\|\[Zend\]\)/{/^zend_extension\(_manager\.guard\)\?\(_ts\)\?=/d;p}' /etc/php/php.ini > /etc/php/conf.d/ZendGuard.ini
	cp -f /etc/php/php.ini{,.rpmsave}
	sed -i -e '/^\(zend_\|\[Zend\]\)/d' /etc/php/php.ini
fi

%files
%defattr(644,root,root,755)
%doc data/doc/* LICENSE
%attr(755,root,root) %{_bindir}/zendid
%dir %{_libdir}/Zend
%dir %{_libdir}/Zend/lib
%dir %{_libdir}/Zend/lib/Guard-%{version}
%dir %{_libdir}/Zend/lib/Guard-%{version}/php-*
%dir %{_libdir}/Zend/lib/Guard_TS-%{version}
%dir %{_libdir}/Zend/lib/Guard_TS-%{version}/php-*
%attr(755,root,root) %{_libdir}/Zend/lib/Guard-%{version}/php-*/ZendGuard.so
%attr(755,root,root) %{_libdir}/Zend/lib/Guard_TS-%{version}/php-*/ZendGuard.so
%attr(755,root,root) %{_libdir}/Zend/lib/ZendExtensionManager.so
%attr(755,root,root) %{_libdir}/Zend/lib/ZendExtensionManager_TS.so
%{_libdir}/Zend/bin
%ghost %{_libdir}/Zend%{_sysconfdir}

%files -n php-%{name}
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/php/conf.d/zendguard.ini
%config %verify(not md5 mtime size) %{_sysconfdir}/php/conf.d/zendguard_pack.ini
%{_sysconfdir}/php/poweredbyguard.gif
