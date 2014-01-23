from lxml import etree
from os import path

from .._base import BaseFinder


class PyCharmFinder(BaseFinder):

    application = 'PyCharm.app'

    _PATH = path.expanduser('~/Library/Preferences/PyCharm30/options/other.xml')
    USER_HOME = path.expanduser('~')

    @staticmethod
    def is_available():
        return path.isfile(PyCharmFinder._PATH)

    def find_items(self, query):
        with open(self._PATH, 'r') as f:
            xml = etree.parse(f)

        root = xml.getroot()

        projects = root.xpath("//component[@name='RecentDirectoryProjectsManager']"
                              "/option[@name='recentPaths']/list/option/@value")

        items = []

        for project_path in projects:
            project_path = project_path.replace('$USER_HOME$', self.USER_HOME)
            project_name = self.get_project_name(project_path)

            items.append(self.create_item(
                project_name,
                project_path
            ))

        return items

    def get_project_name(self, project_path):
        name_file = path.join(project_path, '.idea', '.name')

        project_name = ''

        if path.isfile(name_file):
            with open(name_file, 'r') as f:
                project_name = f.readline().strip()

        if not project_name:
            project_name = path.basename(project_path)

        return project_name