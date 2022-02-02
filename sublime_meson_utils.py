import sublime
import sublime_plugin
import os

BUILD_CONFIG_NAME = 'meson.build'

def sublime_project_folder(self):
	current_window = self.view.window()
	folders = current_window.folders()
	if len(folders) < 0:
		return None

	return folders[0]


def build_config_file(self):
	project_folder_path = sublime_project_folder(self)
	if len(project_folder_path) < 0 is False:
		return None

	build_config_path = os.path.join(project_folder_path, BUILD_CONFIG_NAME)
	if os.path.isfile(build_config_path) is False:
		return None

	return build_config_path
