import sublime
import sublime_plugin
from pathlib import Path

BUILD_CONFIG_NAME = 'meson.build'

def sublime_project_folder(self):
	current_window = self.view.window()
	folders = current_window.folders()
	if len(folders) < 0:
		return None

	return Path(folders[0])


def build_config_path(self):
	project_folder_path = sublime_project_folder(self)
	if project_folder_path is None:
		return None

	config_path = project_folder_path.joinpath(BUILD_CONFIG_NAME)
				      			
	if config_path.is_file() is False:
		return None

	return config_path
