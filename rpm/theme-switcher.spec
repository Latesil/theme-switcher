%global commit      71e219ad0c58a51ac7bc0def992db41454e4fae6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date        20190707

Name:           theme-switcher
Version:        0
Release:        6.beta1.%{date}git%{shortcommit}%{?dist}
Summary:        Switch dark/light GTK theme automatically during day/night

License:        GPLv3+
URL:            https://github.com/Latesil/theme-switcher
Source0:        %{url}/tarball/%{commit}#/%{name}-%{version}.%{date}git%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils

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
mkdir -p %{buildroot}%{_userunitdir}
mv theme-switcher-auto.service  %{buildroot}%{_userunitdir}
mv theme-switcher-auto.timer    %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_datadir}/applications
mv theme-switcher-gui.desktop   %{buildroot}%{_datadir}/applications/
mv theme-switcher.desktop       %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512
mv light-dark-icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/
mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
mv org.theme-switcher.gschema.xml %{buildroot}%{_datadir}/glib-2.0/schemas/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-gui.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
%systemd_user_post %{name}-auto.timer

%preun
%systemd_user_preun %{name}-auto.timer

%postun
%systemd_user_postun_with_restart %{name}-auto.timer

%files
%doc README.md CREDITS
%license LICENSE
%{_bindir}/%{name}-auto.sh
%{_bindir}/%{name}-manual.sh
%{_bindir}/theme-switcher-gui.py
%{_datadir}/applications/%{name}-gui.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.theme-switcher.gschema.xml
%{_datadir}/icons/hicolor/512x512/light-dark-icon.png
%{_userunitdir}/%{name}-auto.service
%{_userunitdir}/%{name}-auto.timer

%changelog
* Sat Jul 06 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-2.beta1.20190706git0b5a714
- Update to latest git snapshot

* Wed Jun 12 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-1.20190612gitceb42e5
- Initial package