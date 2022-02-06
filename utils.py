import sublime
import sublime_plugin
import glob
from pathlib import Path

BUILD_CONFIG_NAME = 'meson.build'
STATUS_MESSAGE_PREFIX = 'Meson'

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