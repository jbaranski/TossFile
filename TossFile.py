import shutil
import sublime
import sublime_plugin

class TossFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        file_name = self.view.file_name()
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
