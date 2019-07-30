project(
	'theme-switcher',
	version: '0.9.1',
	meson_version: '>= 0.50.0',
)

gnome = import('gnome')
i18n  = import('i18n')
python = import('python')

# Module objects
py_installation = python.find_installation('python3')

# Make sure Python is installed and found
if not py_installation.found()
    error('No valid python3 binary found')
endif

APPLICATION_ID = 'com.github.Latesil.theme-switcher'
PYTHON_DIR = py_installation.get_path('purelib')
PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), APPLICATION_ID)
PKGLIB_DIR = join_paths(get_option('prefix'), get_option('libdir'), APPLICATION_ID)
MODULE_DIR = join_paths(PKGDATA_DIR, 'theme-switcher')

bin_config = configuration_data()
bin_config.set('application_id', APPLICATION_ID)
bin_config.set('pkgdatadir', PKGDATA_DIR)
bin_config.set('localedir', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
bin_config.set('pythondir', PYTHON_DIR)
bin_config.set('pyexecdir', py_installation.get_path('stdlib'))
bin_config.set('schemasdir', '')

theme_switcher_sources = [
	'theme_switcher/__init__.py',
	'theme_switcher/bottom_box.py',
	'theme_switcher/header_bar.py',
	'theme_switcher/main_window.py',
  'theme_switcher/middle_box.py',
  'theme_switcher/popover.py',
  'theme_switcher/upper_grid.py'
]

gnome.compile_resources('theme-switcher',
	'theme-switcher.gresource.xml',
	gresource_bundle: true,
	install: true,
	install_dir: PKGDATA_DIR,
)

dependency('gtk+-3.0', version: '>= 3.24.7')

subdir('data')
subdir('po')

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

configure_file(
    input: 'theme-switcher-gui.in',
    output: 'theme-switcher-gui',
    configuration: bin_config,
    install_dir: get_option('bindir')
)

install_data(theme_switcher_sources, install_dir: MODULE_DIR)

meson.add_install_script('build-aux/meson/postinstall.py')