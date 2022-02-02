import sublime
import sublime_plugin

def sublime_project_folder(self):
	current_window = self.view.window()
	folders = current_window.folders()
	if len(folders) < 0:
		return ""

	return folders[0]


def build_config_file(self):
	project_folder_path = sublime_project_folder(self)
	if len(project_folder_path) < 0 is False:
		return ""

	print("Project folder path:", project_folder_path)

		

