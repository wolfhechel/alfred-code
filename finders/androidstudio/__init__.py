from lxml import etree
from os import path

from .._base import BaseFinder

class AndroidStudioFinder(BaseFinder):

    application = 'Android Studio.app'

    _PATH = path.expanduser('~/Library/Preferences/AndroidStudioPreview/options/other.xml')
    USER_HOME = path.expanduser('~')

    @staticmethod
    def is_available():
        return path.isfile(AndroidStudioFinder._PATH)

    def find_items(self, query):
        with open(self._PATH, 'r') as f:
            xml = etree.parse(f)

        root = xml.getroot()

        projects = root.xpath("//component[@name='RecentProjectsManager']"
                              "/option[@name='recentPaths']/list/option/@value")

        items = []

        for project_path in projects:
            project_path = project_path.replace('$USER_HOME$', self.USER_HOME)
            project_name = path.basename(project_path)

            items.append(self.create_item(
                project_name,
                project_path
            ))

        return items