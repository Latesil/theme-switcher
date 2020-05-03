%global uuid    com.github.Latesil.%{name}

Name:           theme-switcher
Version:        1.9.9
Release:        1%{?dist}
Summary:        Switch dark/light GTK theme automatically during day/night

License:        GPLv3+
URL:            https://github.com/Latesil/theme-switcher
Source0:        %{url}/archive/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  desktop-file-utils
BuildRequires:  intltool

%if 0%{?fedora}
BuildRequires:  libappstream-glib
%endif
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(systemd)

Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       python3-gobject

%description
A global automated switcher for dark/light GTK theme during day/night and more.

Theme-switcher automatically can switch your:

- GTK theme
- GNOME Terminal profiles
- Wallpapers
- More will come...

To read docs run:

  xdg-open %{_docdir}/%{name}/README.md


%prep
%autosetup


%build
%meson
%meson_build


%install
%meson_install
%find_lang %{uuid}


%check
%if 0%{?fedora}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
%endif
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files -f %{uuid}.lang
%license LICENSE
%doc README.md CREDITS
%{_bindir}/%{name}-auto.py
%{_bindir}/%{name}-manual.py
%{_bindir}/%{name}-gui
%{python3_sitelib}/Themeswitcher/
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/symbolic/*/*.svg
%{_datadir}/%{name}/
%{_metainfodir}/*.xml
%{_userunitdir}/%{name}-auto.*


%changelog
* Sun May 03 2020 Latesil <vihilantes@gmail.com> - 1.9.9-1
- Update to 1.9.9

* Sat May 02 2020 Latesil <vihilantes@gmail.com> - 1.9.8-1
- Update to 1.9.8

* Sat May 02 2020 Latesil <vihilantes@gmail.com> - 1.9.7-1
- Update to 1.9.7

* Mon Apr 27 2020 Latesil <vihilantes@gmail.com> - 1.9.6-1
- Update to 1.9.6

* Sat Apr 25 2020 Latesil <vihilantes@gmail.com> - 1.9.5-1
- Update to 1.9.5

* Mon Apr 20 2020 Latesil <vihilantes@gmail.com> - 1.9.4-1
- Update to 1.9.4

* Mon Apr 20 2020 Latesil <vihilantes@gmail.com> - 1.9.3-1
- Update to 1.9.3

* Sun Mar 22 2020 Latesil <vihilantes@gmail.com> - 1.9.1-1
- Update to 1.9.1

* Sun Mar 22 2020 Latesil <vihilantes@gmail.com> - 1.9.0-1
- Update to 1.9.0

* Fri Nov 08 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-1.20191109gitf45bd1a
- Update to 1.0.0

* Mon Nov 04 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9.1-1.20191104git7ec63be
- Update to latest git snapshot

* Sat Nov 02 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9.1-1.20191102git0e9c4e0
- Update to latest git snapshot

* Wed Jul 31 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9.1-1.20190801git570f378
- Update to latest git snapshot

* Sun Jul 28 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9-8.20190728gitb1a6284
- Update to latest git snapshot

* Sun Jul 14 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.9-1.20190714git284cadb
- Update to latest git snapshot

* Wed Jun 12 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-1.20190612gitceb42e5
- Initial package
