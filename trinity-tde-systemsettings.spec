%bcond clang 1

# TDE variables
%define tde_pkg tde-systemsettings
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%undefine _debugsource_template

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	14.1.6
Release:	1
Summary:	Easy to use control centre for TDE
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/applications/settings/%{tarball_name}-%{version}.tar.xz
Source1:		tde-settings-laptops.directory


Provides:	trinity-kde-systemsettings = %{EVRD}
Obsoletes:	trinity-kde-systemsettings < %{EVRD}
Provides:	trinity-systemsettings = %{EVRD}
Obsoletes:	trinity-systemsettings < %{EVRD}

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DCONFIG_INSTALL_DIR=%{_sysconfdir}/trinity
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DSYSCONF_INSTALL_DIR=%{_sysconfdir}/trinity
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdebase-devel >= %{version}
BuildRequires:	trinity-tde-cmake >= %{version}

BuildRequires:	desktop-file-utils


%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrender)

Requires:		trinity-guidance >= %{version}


%description
System preferences is a replacement for the TDE
Control Centre with an improved user interface.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%__install -D -m 644 %{SOURCE1} %{buildroot}%{tde_prefix}/share/desktop-directories/tde-settings-laptops.directory

# Unwanted files
%__rm -f %{buildroot}%{tde_prefix}/share/applications/tde/kcmfontinst.desktop
%__rm -f %{buildroot}%{tde_prefix}/share/desktop-directories/tde-settings-power.directory
%__rm -f %{buildroot}%{tde_prefix}/share/desktop-directories/tde-settings-system.directory

%__rm -f %{buildroot}%{tde_prefix}/share/applications/tde/laptop.desktop

echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/audioencoding.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/defaultapplication.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/kcm_knetworkconfmodule_ss.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/medianotifications.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/systemsettings.desktop"

# Fix translation names
for d in "%{buildroot}%{tde_prefix}/share/locale/"*"/LC_MESSAGES"; do
  mv "${d}/"*".mo" "${d}/%{tde_pkg}.mo"
done

%find_lang %{tde_pkg}


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc README.md TODO
%dir %{_sysconfdir}/trinity/xdg
%dir %{_sysconfdir}/trinity/xdg/menus
%dir %{_sysconfdir}/trinity/xdg/menus/applications-merged
%{_sysconfdir}/trinity/xdg/menus/applications-merged/tde-system-settings-merge.menu
%{_sysconfdir}/trinity/xdg/menus/tde-system-settings.menu
%{tde_prefix}/bin/systemsettings
%{tde_prefix}/share/applications/tde/audioencoding.desktop
%{tde_prefix}/share/applications/tde/defaultapplication.desktop
%{tde_prefix}/share/applications/tde/kcm_knetworkconfmodule_ss.desktop
%{tde_prefix}/share/applications/tde/medianotifications.desktop
%{tde_prefix}/share/applications/tde/systemsettings.desktop
%{tde_prefix}/share/apps/systemsettings/
%config(noreplace) %{_sysconfdir}/trinity/systemsettingsrc
%{tde_prefix}/share/desktop-directories/*.directory
%{tde_prefix}/share/icons/crystalsvg/*/apps/systemsettings.png
%{tde_prefix}/share/doc/tde/HTML/en/tde-systemsettings/
%{tde_prefix}/share/man/man1/systemsettings.1*

