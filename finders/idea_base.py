from lxml import etree
from os import path

from ._base import BaseFinder


class IdeaBaseFinder(BaseFinder):

    preferences_folder = None

    USER_HOME = path.expanduser('~')

    xpath = "//component[@name='RecentDirectoryProjectsManager']" \
            "/option[@name='recentPaths']/list/option/@value"

    def find_items(self):
        preferences_file_path = self.get_preferences_file(self.preferences_folder, 'options', 'other.xml')

        with open(preferences_file_path, 'r') as f:
            xml = etree.parse(f)

        root = xml.getroot()

        projects = root.xpath(self.xpath)

        for project_path in projects:
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