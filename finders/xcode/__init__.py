from os import path
import Foundation
from CoreFoundation import CFErrorCopyFailureReason

import workflow

from .._base import BaseFinder


class XCodeFinder(BaseFinder):

    application_id = 'com.apple.dt.Xcode'

    SHARED_FILE_LIST = 'com.apple.dt.Xcode.LSSharedFileList.plist'

    def icon_for_path(self, path):
        return (path, 'fileicon')

    def create_item(self, name, path_or_error, valid=True, icon=None):
        if not valid:
            icon = workflow.ICON_ERROR, ''
        else:
            icon = None

        item_config = super(XCodeFinder, self).create_item(name, path_or_error, valid, icon)

        if not valid:
            item_config.update({
                'arg': 'failure:' + name
            })

        return item_config

    def find_items(self):
        shared_file_list_path = self.get_preferences_file(self.SHARED_FILE_LIST)

        plist = self.open_plist(shared_file_list_path)

        list_items = plist.get('RecentDocuments', {}).get('CustomListItems', {})

        for list_item in list_items:
            information, valid = self.parse_item(list_item)

            if valid:
                name, project_path = information

                if path.exists(project_path):
                    yield self.create_item(
                        name, project_path
                    )
            else:
                name, error_reason = information
                yield self.create_item(
                    name, error_reason, valid=False
                )

    def open_plist(self, plist_path):
        return Foundation.NSDictionary.dictionaryWithContentsOfFile_(plist_path)

    def handle_error(self, error):
        reason = CFErrorCopyFailureReason(error)

        if reason:
            error_description = u'Error: ' + unicode(reason)
        else:
            error_description = u'Unknown error encountered'

        return error_description

    def parse_item(self, item):
        bookmark = item['Bookmark']
        name = item['Name']

        url, error = Foundation.NSURL.alloc().initByResolvingBookmarkData_options_relativeToURL_bookmarkDataIsStale_error_(
            bookmark, (1 << 8), None, None, None
        )[::2]

        valid = url is not None

        if valid:
            information = (name, unicode(url.path()))
        else:
            information = (name, self.handle_error(error))

        return information, valid