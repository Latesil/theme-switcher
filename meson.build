project(
	'theme-switcher',
	version: '0.9.1',
	meson_version: '>= 0.50.0',
)

i18n  = import('i18n')

subdir('data')
subdir('po')
subdir('themeswitcher')

install_data(
  'theme-switcher-auto.service',
  install_dir: join_paths(get_option('prefix'), 'lib/systemd/user')
)

install_data(
  'theme-switcher-auto.timer',
  install_dir: join_paths(get_option('prefix'), 'lib/systemd/user')
)

install_data(
  'theme-switcher-manual.sh',
  install_dir: get_option('bindir')
)

install_data(
  'theme-switcher-auto.sh',
  install_dir: get_option('bindir')
)

meson.add_install_script('build-aux/meson/postinstall.py')
