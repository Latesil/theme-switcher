%global commit      b1a6284b3718d7e7c2b039afde394c65433c60df
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date        20190728

%global appname com.github.Latesil.theme-switcher

Name:           theme-switcher
Version:        0.9
Release:        8.%{date}git%{shortcommit}%{?dist}
Summary:        Switch dark/light GTK theme automatically during day/night

License:        GPLv3+
URL:            https://github.com/Latesil/theme-switcher
Source0:        %{url}/tarball/%{commit}#/%{name}-%{version}.%{date}git%{shortcommit}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  libappstream-glib
BuildRequires:  python3-devel
BuildRequires:  systemd-rpm-macros
Requires:       gtk3%{?_isa}
Requires:       hicolor-icon-theme
Requires:       python3-gobject

%description
A global automated switcher for dark/light GTK theme during day/night and more.

Theme-switcher automatically can switch your:

• GTK theme
• GNOME Terminal profiles
• Wallpapers
• More will come...

To read docs run:

xdg-open %{_docdir}/%{name}/README.md

%prep
%autosetup -n Latesil-%{name}-%{shortcommit}

%install
mkdir -p %{buildroot}%{_bindir}
cp -a %{name}-auto.sh           %{buildroot}%{_bindir}
cp -a %{name}-manual.sh         %{buildroot}%{_bindir}
cp -a %{name}-gui.py            %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{python3_sitelib}/%{name}
cp -a ui                        %{buildroot}%{python3_sitelib}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a %{name}.gresource         %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_userunitdir}
cp -a %{name}-auto.service      %{buildroot}%{_userunitdir}
cp -a %{name}-auto.timer        %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_datadir}/applications
cp -a %{name}-gui.desktop       %{buildroot}%{_datadir}/applications/
cp -a %{name}.desktop           %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
cp -a %{appname}.gschema.xml    %{buildroot}%{_datadir}/glib-2.0/schemas/
# AppData manifest
mkdir -p %{buildroot}%{_metainfodir}
cp -a %{appname}.appdata.xml    %{buildroot}%{_metainfodir}/
# Icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
cp -a icons/%{name}-24.png          %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
cp -a icons/%{name}-32.png          %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
cp -a icons/%{name}-48.png          %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
cp -a icons/%{name}-64.png          %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
cp -a icons/%{name}-96.png          %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
cp -a icons/%{name}-128.png         %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/192x192/apps
cp -a icons/%{name}-192.png         %{buildroot}%{_datadir}/icons/hicolor/192x192/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a icons/%{name}-256.png         %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
cp -a icons/%{name}-512.png         %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
cp -a icons/%{name}-symbolic-16.svg %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps/%{name}-symbolic.svg
# Translation
msgfmt -o po/ru.mo po/ru.po
mkdir -p %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES
cp -a po/ru.mo %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES/%{appname}.mo
%find_lang %{appname}

# %%py_byte_compile %%{__python3} %{buildroot}%{python3_sitelib}/%{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gui.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
# %%systemd_user_post %%{name}-auto.timer

%preun
# %%systemd_user_preun %%{name}-auto.timer

%postun
# %%systemd_user_postun_with_restart %%{name}-auto.timer

%files -f %{appname}.lang
%license LICENSE
%doc README.md CREDITS
%{_bindir}/%{name}-auto.sh
%{_bindir}/%{name}-gui.py
%{_bindir}/%{name}-manual.sh
%{_datadir}/%{name}/%{name}.gresource
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/glib-2.0/schemas/%{appname}.gschema.xml
%{_datadir}/icons/hicolor/*/*/*
%{_metainfodir}/%{appname}.appdata.xml
%{_userunitdir}/%{name}-auto.*
%{python3_sitelib}/%{name}

%changelog
* Sun Jul 28 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9-8.20190728gitb1a6284
- Update to latest git snapshot

* Sun Jul 14 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9-1.20190714git284cadb
- Update to latest git snapshot

* Wed Jun 12 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-1.20190612gitceb42e5
- Initial package
