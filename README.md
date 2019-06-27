# theme-switcher
Switch dark/light GTK theme automatically during day/night

#### Install

Fedora COPR:

```bash
sudo dnf copr enable atim/theme-switcher -y && sudo dnf install theme-switcher -y
```

#### Run

Automatically

```bash
systemctl --user enable --now theme-switcher-auto.timer
```


Manually

```
theme-switcher-manual
```

#### Configure

You need to setup your light/dark profiles in gnome-terminal in order to switch terminal themes automatically. Configure them by edit:

```bash
sudoedit /usr/bin/theme-switcher-auto.sh
```
