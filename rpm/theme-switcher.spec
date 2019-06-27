%global commit      d7724af4fa1fd369922943168e212acc5a652b86
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date        20190612

Name:           theme-switcher
Version:        0
Release:        2.%{date}git%{shortcommit}%{?dist}
Summary:        Switch dark/light GTK theme automatically during day/night

License:        GPLv3+
URL:            https://github.com/tim77/theme-switcher
Source0:        %{url}/tarball/%{commit}#/%{name}-%{version}.%{date}git%{shortcommit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils

Requires:       hicolor-icon-theme

%description
%{summary}.

You need to setup your light/dark profiles in gnome-terminal in order to switch
terminal themes automatically. Configure them by edit:

sudoedit /usr/bin/theme-switcher-auto.sh

%prep
%autosetup -n tim77-%{name}-%{shortcommit}

%install
mkdir -p %{buildroot}%{_bindir}
mv theme-switcher-auto.sh   %{buildroot}%{_bindir}
mv theme-switcher-manual.sh %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_userunitdir}
mv theme-switcher-auto.service  %{buildroot}%{_userunitdir}
mv theme-switcher-auto.timer    %{buildroot}%{_userunitdir}
mkdir -p %{buildroot}%{_datadir}/applications
mv theme-switcher.desktop %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512
mv light-dark-icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
%systemd_user_post %{name}-auto.timer

%preun
%systemd_user_preun %{name}-auto.timer

%postun
%systemd_user_postun_with_restart %{name}-auto.timer

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}-auto.sh
%{_bindir}/%{name}-manual.sh
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/512x512/light-dark-icon.png
%{_userunitdir}/%{name}-auto.service
%{_userunitdir}/%{name}-auto.timer

%changelog
* Wed Jun 12 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0-1.20190612gitceb42e5
- Initial package