import sublime_plugin
import os
from . import sublime_meson_utils

class MesonSetupInputHandler(sublime_plugin.TextInputHandler):
	def name(self):
		return "build_dir"

	def placeholder(self):
		return "Text to insert"


class MesonSetupCommand(sublime_plugin.TextCommand):
    def run(self, edit, build_dir):
    	build_config_file = sublime_meson_utils.build_config_file(self)
    	print("Build config file path:", build_config_file)
    	print("Line:", build_dir)

    def input(self, args):
    	if "build_dir" not in args:
    		return MesonSetupInputHandler()