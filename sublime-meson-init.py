import sublime_plugin

class MesonEchoLineInputHandler(sublime_plugin.TextInputHandler):
	def name(self):
		return "text"

	def placeholder(self):
		return "Text to insert"

class MesonEchoLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, text):
    	print("Line:", text)

    def input(self, args):
    	if "name" not in args:
    		return EchoLineInputHandler()
