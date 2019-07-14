project(
	'theme-switcher',
	version: '0.9.0',
	meson_version: '>= 0.50.0',
)

i18n = import('i18n')

subdir('ui')
subdir('rpm')
subdir('src')
subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')