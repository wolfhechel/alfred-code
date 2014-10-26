import Foundation
import alfred

from .._base import BaseFinder


class XCodeFinder(BaseFinder):

    application_id = 'com.apple.dt.Xcode'

    SHARED_FILE_LIST = 'com.apple.dt.Xcode.LSSharedFileList.plist'

    _open_plist = None

    items = []

    def __init__(self):
        shared_file_list_path = self.get_preferences_file(self.SHARED_FILE_LIST)

        self._open_plist = Foundation.NSDictionary.dictionaryWithContentsOfFile_(shared_file_list_path)

        self.validate_structure()

    def validate_structure(self):
        if 'RecentDocuments' in self._open_plist:
            recent_documents = self._open_plist['RecentDocuments']

            if 'CustomListItems' in recent_documents:
                return

        raise ValueError('Invalid document structure of plist file')

    def icon_for_path(self, path):
        return alfred.Icon(filepath=path)

    def find_items(self, query):
        list_items = self._open_plist.get('RecentDocuments', {}).get('CustomListItems', {})

        for list_item in list_items:
            name, path = self.parse_item(list_item)
            self.items.append(self.create_item(
                name, path
            ))

        return self.items

    def parse_item(self, item):
        bookmark = item['Bookmark']
        name = item['Name']

        url, failure, error = Foundation.NSURL.alloc().initByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
            bookmark, (1 << 8), None, None, None
        )

        return (name, unicode(url.path()))