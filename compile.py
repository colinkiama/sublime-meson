import sublime
import sublime_plugin
import json
import subprocess
from pathlib import Path
from . import utils

build_dirs = []
build_dir_names = []

class MesonCompileInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "selected_option"


    def list_items(self):
        self.clear_build_dir_lists()
        introspection_data_files = utils.introspection_data_files()
        print("introspection_data_files:", introspection_data_files)
        if len(introspection_data_files) < 1:
            return build_dir_names

        for file in introspection_data_files:
            try:
                introspection_data = json.load( open(file) )
                loaded_build_dir = Path(introspection_data["directories"]["build"])
                print("build directory:", loaded_build_dir)
                build_dirs.append(loaded_build_dir)
                build_dir_names.append(loaded_build_dir.stem)
            except Exception as e:
                raise e

        return build_dir_names

    def clear_build_dir_lists(self):
        del build_dirs[:]
        del build_dir_names[:]

    def validate(self, value):
        return len(value.strip()) > 0

class MesonCompileCommand(sublime_plugin.WindowCommand):
    def run(self, build_dir = None, selected_option = None):

        if build_dir is None:
            selected_index = build_dir_names.index(selected_option)
            build_dir = str(build_dirs[selected_index])
        
        self.build_dir = build_dir
      
        sublime.set_timeout_async(self.__run_async, 0)

    def __run_async(self):
        print("build_dir:", self.build_dir)

        subprocess.run(['meson', 'compile', '-C', self.build_dir],
            cwd = utils.project_folder())

    def input (self, args):
        if "selected_option" not in args:
            return MesonCompileInputHandler()