import sublime
import sublime_plugin
import os
import subprocess
from . import utils

class MesonSetupInputHandler(sublime_plugin.TextInputHandler):
    def name(self):
        return "build_dir"

    def placeholder(self):
        return "Text to insert"

    def validate(self, value):
        return len(value.strip()) > 0           

class MesonSetupCommand(sublime_plugin.WindowCommand):
    def run(self, build_dir):
        self.build_dir = build_dir
        self.build_config_path = utils.build_config_path(self)
        if self.build_config_path is None:
            return

        sublime.set_timeout_async(self.__run_async, 0)

    def __run_async(self):
        print("Build config file path:", str(self.build_config_path))
        print("build_dir:", self.build_dir)

        subprocess.run(['meson', 'setup', self.build_dir],
            cwd = utils.project_folder(self))

    def input(self, args):
        if "build_dir" not in args:
            return MesonSetupInputHandler()
