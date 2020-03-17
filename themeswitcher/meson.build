pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'themeswitcher')
gnome = import('gnome')

gnome.compile_resources(meson.project_name(),
	'ui/' + meson.project_name() + '.gresource.xml',
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
  input: meson.project_name() + '-gui.in',
  output: meson.project_name() + '-gui',
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
	'main.py',
	'desktop.py',
	'gnome.py',
]

install_data(theme_switcher_sources, install_dir: moduledir)
