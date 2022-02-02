import sublime_plugin
import os
import subprocess
from . import utils


class MesonSetupInputHandler(sublime_plugin.TextInputHandler):
	def name(self):
		return "build_dir"

	def placeholder(self):
		return "Text to insert"

class MesonSetupCommand(sublime_plugin.WindowCommand):
    def run(self, build_dir):
    	build_config_path = sublime_meson_utils.build_config_path(self)
    	if build_config_path is None:
    		return

    	print("Build config file path:", str(build_config_path))
    	print("build_dir:", build_dir)

    	subprocess.run(['meson', 'setup', build_dir],
    		cwd = sublime_meson_utils.project_folder(self))

    def input(self, args):
    	if "build_dir" not in args:
    		return MesonSetupInputHandler()
