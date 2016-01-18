import os
import shutil
import sublime
import sublime_plugin
import time


class BaseTossFile(sublime_plugin.TextCommand):
    def init_toss(self, toss_type):
        self.toss_file_type = toss_type
        self.num_files_tossed = 0
        self.num_locations_tossed = 0

    def get_status_timeout(self):
        timeout = sublime.load_settings("TossFile.sublime-settings").get("statusTimeout", 0)
        if not isinstance(timeout, int) or timeout == 0:
            timeout = 5
        timeout = timeout * 1000
        return timeout

    def update_status(self):
        self.view.set_status("toss_file_status", self.toss_file_type + ": tossed " + str(self.num_files_tossed) + " file(s) to " + str(self.num_locations_tossed) + " location(s)")
        sublime.set_timeout(lambda: self.clear_status(), self.get_status_timeout())

    def clear_status(self):
        self.view.set_status("toss_file_status", "")

    def toss(self, file_name):
        is_file_tossed = False
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
                        self.num_locations_tossed = self.num_locations_tossed + 1
                        if not is_file_tossed:
                            self.num_files_tossed = self.num_files_tossed + 1
                            is_file_tossed = True


class TossFileCommand(BaseTossFile):
    def run(self, edit, **kwargs):
        self.init_toss("Toss File")
        self.toss(self.view.file_name())
        self.update_status()


class TossAllFilesCommand(BaseTossFile):
    def run(self, edit, **kwargs):
        self.init_toss("Toss All Files")
        open_views = self.view.window().views()
        for x in open_views:
            self.toss(x.file_name())
        self.update_status()
