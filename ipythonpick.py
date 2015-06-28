import os
import sublime
import sublime_plugin
import inspect


LIMIT = 3


class IpythonPickCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        project_data = sublime.active_window().project_data()
        for folder in project_data['folders']:
            ipython_log_path = os.path.join(folder['path'], 'ipython_log.py')
            if os.path.exists(ipython_log_path):
                with open(ipython_log_path, 'r') as f:
                    options = [l.strip() for l in f.readlines()[-LIMIT:]]
                break
        else:
            options = []

        def sel(index):
            text = options[index]
            self.view.run_command("insert", {"characters": text})

        print(type(edit))
        print(inspect.getfile(type(edit)))

        self.view.show_popup_menu(options, sel)
