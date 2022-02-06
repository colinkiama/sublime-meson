import sublime
import sublime_plugin
import glob
import os
from pathlib import Path

BUILD_CONFIG_NAME = 'meson.build'
STATUS_MESSAGE_PREFIX = 'Meson'

panels = {'sublime-meson': None}

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
	# panel = get_panel("sublime-meson")
	panel = sublime.active_window().create_output_panel("sublime-meson")
	sublime.active_window().run_command("show_panel", {"panel": "output.sublime-meson"})
	panel.set_read_only(False)
	env = os.environ
	env["COLORTERM"] = "nocolor"
	cmd_action(panel, env)
	panel.set_read_only(True)
	# panel.run_command('append', {'characters': 'bruh: ' + count, "force": True, "scroll_to_end": True})

def get_panel(key):
	panel = panels[key]
	if panel:
		return panel

	panel = sublime.active_window().create_output_panel(key)
	panels[key] = panel

	return panel
