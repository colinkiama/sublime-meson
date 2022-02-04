import sublime
import sublime_plugin
import os
import subprocess
from . import utils

build_dir_request = {
    'arg': "build_dir", 
    'placeholder': 'Build directory path',
}

prefix_request = {
    'arg': "prefix", 
    'placeholder': 'Prefix (Leave blank for default value)',
}

class MesonSetupInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, request):
        self._name = request["arg"]
        self._placeholder = request["placeholder"]

    def name(self):
        return self._name

    def placeholder(self):
        return self._placeholder

    def validate(self, value):
        if self._name == "prefix":
            return True

        return len(value.strip()) > 0

class MesonSetupCommand(sublime_plugin.WindowCommand):
    def run(self, prefix, build_dir):
        self.build_dir = build_dir
        self.build_config_path = utils.build_config_path()
        if self.build_config_path is None:
            return

        if len(prefix) < 1:
            self.prefix = None
        else:
            self.prefix = prefix

        sublime.set_timeout_async(self.__run_async, 0)

    def __run_async(self):
        command_args = ['meson', 'setup']
        if self.prefix is not None:
            command_args.append("--prefix=" + self.prefix)
        
        command_args.append(self.build_dir)
        subprocess.run(command_args, cwd = utils.project_folder())

    def input(self, args):
        input_requests = []
        if "build_dir" not in args:
            input_requests.append(build_dir_request)

        if "prefix" not in args:
            input_requests.append(prefix_request)
        
        for input_request in input_requests:
            return MesonSetupInputHandler(input_request)
