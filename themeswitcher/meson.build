pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'themeswitcher')
gnome = import('gnome')

gnome.compile_resources(meson.project_name(),
	'ui/' + meson.project_name() + '.gresource.xml',
	gresource_bundle: true,
	install: true,
	install_dir: pkgdatadir,
)

python_mod = import('python')
python3 = python_mod.find_installation()
py_purelib_path = python3.get_path('purelib')

conf = configuration_data()
conf.set('PYTHON', python3.path())
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

install_subdir(
  'Themeswitcher', 
  install_dir: py_purelib_path
)

install_data(
  'theme-switcher-manual.py',
  install_dir: get_option('bindir')
)

install_data(
  'theme-switcher-auto.py',
  install_dir: get_option('bindir')
)

install_data(
  'Themeswitcher/desktop.py',
  install_dir: join_paths(py_purelib_path, 'Themeswitcher')
)

install_data(
  'Themeswitcher/gnome.py',
  install_dir: join_paths(py_purelib_path, 'Themeswitcher')
)

install_data(
  'Themeswitcher/helper_functions.py',
  install_dir: join_paths(py_purelib_path, 'Themeswitcher')
)

install_data(
  'Themeswitcher/theme_switcher_constants.py',
  install_dir: join_paths(py_purelib_path, 'Themeswitcher')
)

theme_switcher_sources = [
	'__init__.py',
	'theme-switcher-auto.py',
	'theme-switcher-manual.py',
	'Themeswitcher/theme_switcher_constants.py',
	'Themeswitcher/helper_functions.py',
	'Themeswitcher/gnome.py',
	'Themeswitcher/desktop.py',
	'new_main_window.py',
	'main.py',
]

install_data(theme_switcher_sources, install_dir: moduledir)
