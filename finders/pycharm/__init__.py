from ..idea_base import IdeaBaseFinder


class PyCharmFinder(IdeaBaseFinder):

    application_id = 'com.jetbrains.pycharm'

    preferences_folder = 'PyCharm*'