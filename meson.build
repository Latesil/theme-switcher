project(
	'theme-switcher',
	version: '0.9.1',
	meson_version: '>= 0.50.0',
)

# Importing modules
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

# Install the executable file
bin_config = configuration_data()
bin_config.set('application_id', APPLICATION_ID)
bin_config.set('pkgdatadir', PKGDATA_DIR)
bin_config.set('localedir', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
bin_config.set('pythondir', PYTHON_DIR)
bin_config.set('pyexecdir', py_installation.get_path('stdlib'))
bin_config.set('schemasdir', '')

dependency('gtk+-3.0', version: '>= 3.24.7')

subdir('data')
subdir('po')

install_subdir(
    'theme_switcher',
    install_dir: py_installation.get_install_dir()
)

install_data(
  'theme-switcher-auto.service',
  install_dir: 'lib/systemd/user'
)

install_data(
  'theme-switcher-auto.timer',
  install_dir: 'lib/systemd/user'
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

meson.add_install_script('build-aux/meson/postinstall.py')