from ..idea_base import IdeaBaseFinder


class AndroidStudioFinder(IdeaBaseFinder):

    application_id = 'com.google.android.studio'

    preferences_folder = 'AndroidStudioPreview'

    xpath = "//component[@name='RecentProjectsManager']" \
            "/option[@name='recentPaths']/list/option/@value"