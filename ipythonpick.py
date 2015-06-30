import inspect
from os import path
import string

import sublime
import sublime_plugin


LIMIT = 30
IPYTHON_LOG = 'ipython_log.py'


def get_raw_log_entries(ipython_log_contents, limit=None):
    entries = []
    buffer = []

    def clear():
        if buffer:
            entries.append('\n'.join(buffer))
            buffer[:] = []

    def is_empty_line(line):
        return not line or line.strip().startswith('#')

    lines = iter(ipython_log_contents.splitlines())
    try:
        while True:
            line = next(lines)
            if is_empty_line(line):
                # we could just continue,
                # but let's be resilient to user added blank lines
                clear()
            elif line[0] in string.whitespace:
                # it is a block, accumulate until an empty line
                while not is_empty_line(line):
                    buffer.append(line)
                    line = next(lines)
                clear()
            else:
                clear()
                buffer.append(line)
    except StopIteration:
        clear()
    entries.reverse()
    return entries[:limit]


class IpythonPickCommand(sublime_plugin.TextCommand):

    def search_folders(self):
        # project folders
        project_data = sublime.active_window().project_data()
        if project_data:
            for folder in project_data.get('folders', []):
                yield folder['path']
        # climb path
        fname = self.view.file_name()
        while True:
            folder = path.dirname(fname)
            if fname == folder:
                break  # hit file system root
            else:
                yield folder
                fname = folder

    def run(self, edit):
        for folder in self.search_folders():
            ipylog = path.join(folder, IPYTHON_LOG)
            if path.exists(ipylog):
                break
            else:
                ipylog = None

        with open(ipylog, 'r') as f:
            options = get_raw_log_entries(f.read(), LIMIT)

        def sel(index):
            if index > -1:
                text = options[index]
                self.view.run_command("insert", {"characters": text})

        print(type(edit))
        print(inspect.getfile(type(edit)))

        self.view.show_popup_menu(options, sel)
