import inspect
from os import path

import sublime
import sublime_plugin


LIMIT = 20
IPYLOG = 'ipython_log.py'


class IpythonPickCommand(sublime_plugin.TextCommand):

    def search_folders(self):
        # project folders
        project_data = sublime.active_window().project_data()
        if project_data:
            for folder in project_data.get('folders', []):
                yield folder['path']
        # climb path
        fname = self.view.fname()
        while True:
            folder = path.dirname(fname)
            if fname == folder:
                break  # hit file system root
            else:
                yield folder
                fname = folder

    def run(self, edit):
        for folder in self.search_folders():
            ipylog = path.join(folder, 'ipython_log.py')
            if path.exists(ipylog):
                break
            else:
                ipylog = None

        with open(ipylog, 'r') as f:
            options = [l.strip() for l in f.readlines()[-LIMIT:]]

        def sel(index):
            text = options[index]
            self.view.run_command("insert", {"characters": text})

        print(type(edit))
        print(inspect.getfile(type(edit)))

        self.view.show_popup_menu(options, sel)
