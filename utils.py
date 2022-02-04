import sublime
import sublime_plugin
import glob
from pathlib import Path

BUILD_CONFIG_NAME = 'meson.build'

def project_folder(context):
	current_window = context.window
	folders = current_window.folders()
	if len(folders) < 0:
		return None

	return Path(folders[0])


def build_config_path(context):
	project_folder_path = project_folder(context)
	if project_folder_path is None:
		return None

	config_path = project_folder_path.joinpath(BUILD_CONFIG_NAME)
				      			
	if config_path.is_file() is False:
		return None

	return config_path

def find_introspection_data(context):
	results = []
	current_project_folder = project_folder(context)
	if current_project_folder is None:
		return

	return glob.glob(str(current_project_folder) + '/*/meson-info/meson-info.json')
