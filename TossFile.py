from string import Template
import os
import shutil
import sublime
import sublime_plugin


class BaseTossFile(sublime_plugin.TextCommand):
    def init_toss(self, toss_type):
        self.toss_file_type = toss_type
        self.num_files_tossed = 0
        self.num_locations_tossed = 0
        self.num_files_skipped = 0
        self.num_locations_skipped = 0

    def get_status_timeout(self):
        timeout = sublime.load_settings("TossFile.sublime-settings").get("statusTimeout", 0)
        if not isinstance(timeout, int) or timeout == 0:
            timeout = 5
        timeout = timeout * 1000
        return timeout

    def get_status_str(self):
        toss_file_str = "file" if self.num_files_tossed == 1 else "files"
        toss_location_str = "location" if self.num_locations_tossed == 1 else "locations"
        skip_file_str = "file" if self.num_files_skipped == 1 else "files"
        skip_location_str = "location" if self.num_locations_skipped == 1 else "locations"
        tmpl = "$toss_file_type: tossed $num_files_tossed $toss_file_str to $num_locations_tossed $toss_location_str"
        if self.num_files_skipped > 0:
            tmpl = tmpl + "; settings made toss skip $num_files_skipped $skip_file_str at $num_locations_skipped $skip_location_str"
        status_template_str = Template(tmpl)
        return status_template_str.substitute(toss_file_type=self.toss_file_type,
                                              num_files_tossed=str(self.num_files_tossed),
                                              toss_file_str=toss_file_str,
                                              num_locations_tossed=str(self.num_locations_tossed),
                                              toss_location_str=toss_location_str,
                                              num_files_skipped=str(self.num_files_skipped),
                                              skip_file_str=skip_file_str,
                                              num_locations_skipped=str(self.num_locations_skipped),
                                              skip_location_str=skip_location_str)

    def update_status(self):
        self.view.set_status("toss_file_status", self.get_status_str())
        sublime.set_timeout(lambda: self.clear_status(), self.get_status_timeout())

    def clear_status(self):
        self.view.set_status("toss_file_status", "")

    def skip(self, copy_from, copy_to):
        return self.skip_existing_file(copy_to) or self.skip_name(copy_to) or self.skip_extension(copy_to) or self.skip_path("outputPathExcludes", copy_to) or self.skip_path("inputPathExcludes", copy_from)

    def skip_existing_file(self, copy_to):
        skip = False
        replace_if_exists = sublime.load_settings("TossFile.sublime-settings").get("replaceIfExists", True)
        if type(replace_if_exists) != bool:
            replace_if_exists = True
        if not replace_if_exists:
            if os.path.isfile(copy_to):
                skip = True
        return skip

    def skip_name(self, copy_to):
        skip = False
        name_excludes = sublime.load_settings("TossFile.sublime-settings").get("nameExcludes", [])
        file_name = os.path.basename(copy_to)
        for name in name_excludes:
            if file_name == name:
                skip = True
                break
        return skip

    def skip_extension(self, copy_to):
        skip = False
        extension_excludes = sublime.load_settings("TossFile.sublime-settings").get("extensionExcludes", [])
        file_extension = os.path.splitext(copy_to)[1]
        if file_extension:
            for extension in extension_excludes:
                if file_extension == extension:
                    skip = True
                    break
        return skip

    def skip_path(self, settingKey, target):
        skip = False
        paths = sublime.load_settings("TossFile.sublime-settings").get(settingKey, [])
        for path in paths:
            if target.startswith(path):
                skip = True
                break
        return skip

    def toss(self, file_name):
        is_file_tossed = False
        is_file_skipped = False
        if file_name:
            paths = sublime.load_settings("TossFile.sublime-settings").get("paths", [])
            for path in paths:
                for source, destination in path.items():
                    if file_name.startswith(source):
                        copy_to = file_name.replace(source, destination)
                        if self.skip(file_name, copy_to):
                            self.num_locations_skipped = self.num_locations_skipped + 1
                            if not is_file_skipped:
                                self.num_files_skipped = self.num_files_skipped + 1
                                is_file_skipped = True
                        else:
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
