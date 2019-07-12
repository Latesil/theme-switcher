%global commit      18057fd136f0d53fe7228b56c7d777fa0c4540c4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date        20190712

%global appname     com.github.Latesil.theme-switcher

Name:           theme-switcher
Version:        0
Release:        14.beta1.ui.%{date}git%{shortcommit}%{?dist}
Summary:        Switch dark/light GTK theme automatically during day/night

License:        GPLv3+
URL:            https://github.com/Latesil/theme-switcher
Source0:        %{url}/tarball/%{commit}#/%{name}-%{version}.%{date}git%{shortcommit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  python3-devel
BuildRequires:  systemd-rpm-macros
Requires:       gtk3
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

xdg-open /usr/share/doc/theme-switcher/README.md

%prep
%autosetup -n Latesil-%{name}-%{shortcommit}

%install
mkdir -p %{buildroot}%{_bindir}
mv theme-switcher-auto.sh   %{buildroot}%{_bindir}
mv theme-switcher-manual.sh %{buildroot}%{_bindir}
mv theme-switcher-gui.py    %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{python3_sitelib}/%{name}
mv ui                       %{buildroot}%{python3_sitelib}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}
mv theme-switcher.gresource     %{buildroot}%{_datadir}/%{name}/
mkdir -p %{buildroot}%{_userunitdir}
mv theme-switcher-auto.service  %{buildroot}%{_userunitdir}
mv theme-switcher-auto.timer    %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_datadir}/applications
mv theme-switcher-gui.desktop   %{buildroot}%{_datadir}/applications/
mv theme-switcher.desktop       %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512
mv light-dark-icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
mv com.github.Latesil.theme-switcher.gschema.xml %{buildroot}%{_datadir}/glib-2.0/schemas/
# Translation
msgfmt -o po/ru.mo po/ru.po
mkdir -p    %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES
mv po/ru.mo %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES/%{appname}.mo
%find_lang %{appname}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gui.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
%systemd_user_post %{name}-auto.timer

%preun
%systemd_user_preun %{name}-auto.timer

%postun
%systemd_user_postun_with_restart %{name}-auto.timer

%files -f %{appname}.lang
%doc README.md CREDITS
%license LICENSE
%{_bindir}/%{name}-auto.sh
%{_bindir}/%{name}-gui.py
%{_bindir}/%{name}-manual.sh
%{_datadir}/%{name}/%{name}.gresource
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/%{appname}.gschema.xml
%{_datadir}/icons/hicolor/512x512/light-dark-icon.png
%{_userunitdir}/%{name}-auto.service
%{_userunitdir}/%{name}-auto.timer
%{python3_sitelib}/%{name}

%changelog
* Sat Jul 06 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-2.beta1.20190706git0b5a714
- Update to latest git snapshot

* Wed Jun 12 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-1.20190612gitceb42e5
- Initial package
