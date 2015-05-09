try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET

from os import path
from glob import glob

from ._base import BaseFinder


class IdeaBaseFinder(BaseFinder):

    preferences_folder = None

    USER_HOME = path.expanduser('~')

    xpath = ".//component[@name='RecentDirectoryProjectsManager']" \
            "/option[@name='recentPaths']/list/option"

    def expand_preferences_folder(self):
        glob_path = path.join(self._user_preferences_path, self.preferences_folder)

        matches = glob(glob_path)

        return matches[-1] if matches else glob_path

    possible_file_paths = [
        ('options', 'recentProjectDirectories.xml'),
        ('options', 'other.xml'),
    ]

    def find_items(self):
        preferences_folder = self.workflow.cached_data(
            self.preferences_folder,
            self.expand_preferences_folder,
            max_age=60 * 60 * 24
        )

        def find_preferences_file_path():
            for possible_file_path in self.possible_file_paths:
                file_path = path.join(preferences_folder, *possible_file_path)

                if path.exists(file_path):
                    return file_path

        preferences_file_path = self.workflow.cached_data(
            self.preferences_folder + 'file_path',
            find_preferences_file_path,
            max_age=60 * 60 * 24
        )

        if preferences_file_path:
            xml = ET.parse(preferences_file_path)

            projects = xml.findall(self.xpath)

            for project in projects:
                project_path = project.get('value')
                project_path = project_path.replace('$USER_HOME$', self.USER_HOME)

                if path.exists(project_path):
                    project_name = self.get_project_name(project_path)

                    yield self.create_item(
                        project_name,
                        project_path
                    )

    def get_project_name(self, project_path):
        name_file = path.join(project_path, '.idea', '.name')

        project_name = ''

        if path.isfile(name_file):
            with open(name_file, 'r') as f:
                project_name = f.readline().strip()

        if not project_name:
            project_name = path.basename(project_path)

        return project_name