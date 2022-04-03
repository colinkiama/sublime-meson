import sublime
import sublime_plugin
import glob
import os
from pathlib import Path

BUILD_CONFIG_NAME = 'meson.build'
STATUS_MESSAGE_PREFIX = 'Meson'

panels = {'meson': None}

def _test_paths_for_executable(paths, test_file):
    for directory in paths:
        file_path = os.path.join(directory, test_file)
        if os.path.exists(file_path) and os.access(file_path, os.X_OK):
            return file_path


def find_binary(cmd):
    path = os.environ.get('PATH', '').split(os.pathsep)
    if os.name == 'nt':
        cmd = cmd + '.exe'

    path = _test_paths_for_executable(path, cmd)

    if not path:
        # /usr/local/bin:/usr/local/meson/bin
        if os.name == 'nt':
            extra_paths = (
                os.path.join(os.environ.get("ProgramFiles", ""), "meson", "bin"),
                os.path.join(os.environ.get("ProgramFiles(x86)", ""), "meson", "bin"),
            )
        else:
            extra_paths = (
                '/usr/local/bin',
                '/usr/local/meson/bin',
            )
        path = _test_paths_for_executable(extra_paths, cmd)
    return path

MESON_BINARY = find_binary('meson')

def project_folder():
	folders = sublime.active_window().folders()
	if len(folders) < 0:
		return None

	return Path(folders[0])


def build_config_path():
	project_folder_path = project_folder()
	if project_folder_path is None:
		return None

	config_path = project_folder_path.joinpath(BUILD_CONFIG_NAME)
				      			
	if config_path.is_file() is False:
		return None

	return config_path

def introspection_data_files():
	results = []
	current_project_folder = project_folder()
	if current_project_folder is None:
		return results

	return glob.glob(str(current_project_folder) + '/*/meson-info/meson-info.json')

def display_status_message(message):
	sublime.active_window().status_message(STATUS_MESSAGE_PREFIX + ': '  + message)

def update_output_panel(cmd_action):
	panel = sublime.active_window().create_output_panel("meson")
	sublime.active_window().run_command("show_panel", {"panel": "output.meson"})
	panel.set_read_only(False)
	env = os.environ
	env["COLORTERM"] = "nocolor"
	cmd_action(panel, env)
	panel.set_read_only(True)
