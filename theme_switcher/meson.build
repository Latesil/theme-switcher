pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'theme_switcher')
gnome = import('gnome')

gnome.compile_resources('theme-switcher',
	'ui/theme-switcher.gresource.xml',
	gresource_bundle: true,
	install: true,
	install_dir: pkgdatadir,
)

python3 = import('python3')

conf = configuration_data()
conf.set('PYTHON', python3.find_python().path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'theme-switcher-gui.in',
  output: 'theme-switcher',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

theme_switcher_sources = [
	'__init__.py',
	'bottom_box.py',
	'main_window.py',
	'header_bar.py',
    'helper_functions.py',
    'middle_box.py',
    'popover.py',
    'theme_switcher_constants.py',
    'upper_grid.py',
]

install_data(theme_switcher_sources, install_dir: moduledir)