from os import path

from Foundation import *
from .._base import BaseFinder


class InvalidItem(Exception):
    pass


class XCodeFinder(BaseFinder):

    application = 'Xcode.app'

    _PATH = path.expanduser('~/Library/Preferences/com.apple.dt.Xcode.LSSharedFileList.plist')

    _open_plist = None

    items = []

    def __init__(self):
        self._open_plist = NSDictionary.dictionaryWithContentsOfFile_(self._PATH)

        self.validate_structure()


    def validate_structure(self):
        if 'RecentDocuments' in self._open_plist:
            recent_documents = self._open_plist['RecentDocuments']

            if 'CustomListItems' in recent_documents:
                return

        raise ValueError('Invalid document structure of plist file')

    @staticmethod
    def is_available():
        return path.isfile(XCodeFinder._PATH)

    def find_items(self, query):
        list_items = self._open_plist['RecentDocuments']['CustomListItems']

        for list_item in list_items:
            name, path = self.parse_item(list_item)
            self.items.append(self.create_item(
                name, path
            ))

        return self.items

    def parse_item(self, item):
        bookmark = item['Bookmark']
        name = item['Name']

        url, failure, error = NSURL.alloc().initByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
            bookmark, (1 << 8), None, None, None
        )

        return (name, unicode(url.path()))