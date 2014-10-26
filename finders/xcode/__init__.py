from os import path
import Foundation

from .._base import BaseFinder


class XCodeFinder(BaseFinder):

    application_id = 'com.apple.dt.Xcode'

    SHARED_FILE_LIST = 'com.apple.dt.Xcode.LSSharedFileList.plist'

    def icon_for_path(self, path):
        return (path, 'fileicon')

    def find_items(self):
        shared_file_list_path = self.get_preferences_file(self.SHARED_FILE_LIST)

        plist = self.open_plist(shared_file_list_path)

        list_items = plist.get('RecentDocuments', {}).get('CustomListItems', {})

        for list_item in list_items:
            name, project_path = self.parse_item(list_item)

            if path.exists(project_path):
                yield self.create_item(
                    name, project_path
                )

    def open_plist(self, plist_path):
        return Foundation.NSDictionary.dictionaryWithContentsOfFile_(plist_path)

    def parse_item(self, item):
        bookmark = item['Bookmark']
        name = item['Name']

        url, failure, error = Foundation.NSURL.alloc().initByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
            bookmark, (1 << 8), None, None, None
        )

        return (name, unicode(url.path()))