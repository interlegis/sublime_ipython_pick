import code
from os import path

import sublime
import sublime_plugin


LIMIT = 30
IPYTHON_LOG = 'ipython_log.py'


def get_sentences(lines, limit=None):
    sentence_list = []
    partial = ''

    def collect():
        sentence = str(partial.strip())
        if sentence and not sentence.startswith('#'):
            sentence_list.append(sentence)

    for line in lines:
        partial += line
        try:
            compiled = code.compile_command(partial)
        except (SyntaxError, ValueError, OverflowError):
            partial = ''  # discard and reset
        else:
            if compiled:
                collect()
                partial = ''  # reset
    collect()
    sentence_list.reverse()
    return sentence_list[:limit]


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
            options = get_sentences(f.readlines(), LIMIT)

        def sel(index):
            if index > -1:
                text = options[index]
                self.view.run_command("insert", {"characters": text})

        self.view.show_popup_menu(options, sel)
