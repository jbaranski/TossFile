import os
import shutil
import sublime
import sublime_plugin

class BaseTossFile(sublime_plugin.TextCommand):
    def toss(self, file_name):
        if file_name:
            paths = sublime.load_settings("TossFile.sublime-settings").get("paths", [])
            for path in paths:
                for source, destination in path.items():
                    if file_name.startswith(source):
                        copy_to = file_name.replace(source, destination)
                        copy_to_dir = os.path.dirname(copy_to)
                        if not os.path.exists(copy_to_dir):
                            os.makedirs(copy_to_dir)
                        shutil.copyfile(file_name, copy_to)

class TossFileCommand(BaseTossFile):
    def run(self, edit, **kwargs):
        self.toss(self.view.file_name())

class TossAllFilesCommand(BaseTossFile):
    def run(self, edit, **kwargs):
        open_views = self.view.window().views()
        for x in open_views:
            self.toss(x.file_name())