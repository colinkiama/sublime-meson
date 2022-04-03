import sublime
import sublime_plugin
import json
import subprocess
import os
import importlib

from pathlib import Path
from . import utils


build_dirs = []
build_dir_names = []

importlib.import_module('Meson')

class MesonCompileInputHandler(sublime_plugin.ListInputHandler):
    def name(self):
        return "selected_option"

    def list_items(self):
        self.clear_build_dir_lists()
        introspection_data_files = utils.introspection_data_files()
        if len(introspection_data_files) < 1:
            return build_dir_names

        for file in introspection_data_files:
            try:
                introspection_data = json.load( open(file) )
                loaded_build_dir = Path(introspection_data["directories"]["build"])
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
        utils.display_status_message("Compiling from:" + self.build_dir)
        command_args = [utils.MESON_BINARY, 'compile', '-C', self.build_dir]

        def cmd_action(panel, env):
            process = subprocess.Popen(" ".join(command_args), stdout = subprocess.PIPE, shell = True, cwd = utils.project_folder(), env = env, bufsize = 0)
            if process:
                process.stdout.flush()
                for line in iter(process.stdout.readline, b''):
                    panel.run_command('append', {'characters': line.decode('utf-8'), "force": True, "scroll_to_end": True})
                    process.stdout.flush()
                
                process.communicate()   
                
            if process.returncode == 0:
                utils.display_status_message("Project Compiled successfully")
            else:
                utils.display_status_message("Project failed to compile, please" +
                    " refer to output panel")

        utils.update_output_panel(lambda panel, env: cmd_action(panel, env))

    def input (self, args):
        if "selected_option" not in args:
            return MesonCompileInputHandler()
