from os import path
import json

from .._base import BaseFinder


class SublimeTextFinder(BaseFinder):

    application_id = 'com.sublimetext.3'

    sublime_application_path = path.expanduser('~/Library/Application Support/Sublime Text 3/Local')

    def load_json_file(self, json_file):
        json_data = None

        if path.exists(json_file):
            with open(json_file, 'r') as fh:
                json_data = json.load(fh, strict=False) # Sublime doesn't properly encode their control characters

        return json_data

    def find_subl_path(self):
        import AppKit

        workspace = AppKit.NSWorkspace.sharedWorkspace()

        app_path = workspace.fullPathForApplication_(self.app_name)

        subl_path = path.join(app_path, 'Contents', 'SharedSupport', 'bin', 'subl')

        return subl_path

    def open_command(self, project_path):
        return (self.find_subl_path(), '--project', project_path)

    def find_items(self):
        sublime_session_path = path.join(self.sublime_application_path, 'Session.sublime_session')

        sublime_data = self.load_json_file(sublime_session_path)

        recent_workspaces = sublime_data.get('workspaces', {}).get('recent_workspaces')

        for workspace in recent_workspaces:
            project_pure_path, _ext = path.splitext(workspace)
            project_path = '.'.join((project_pure_path, 'sublime-project'))

            if path.exists(project_path):
                project_name = path.basename(project_path)
                
                yield self.create_item(project_name,
                                       project_path)