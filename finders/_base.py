import alfred
from os import path
import AppKit
import Foundation
import subprocess

workspace = AppKit.NSWorkspace.sharedWorkspace()

def query_application_id_for_name_and_icon(application_id):
    bundle_path = workspace.absolutePathForAppBundleWithIdentifier_(application_id)

    if bundle_path:
        bundle = Foundation.NSBundle.bundleWithPath_(bundle_path)
    else:
        bundle = None

    if not bundle:
        raise ValueError('Application {} not found in the system'.format(application_id))

    info_dictionary = bundle.infoDictionary()

    icon_file_name = info_dictionary.get('CFBundleIconFile')

    icon_path = ''
    if icon_file_name:
        icon_path = bundle.pathForImageResource_(icon_file_name)

    name = info_dictionary.get('CFBundleName')

    return (name, icon_path)


class FinderType(type):
    def __new__(cls, name, bases, dict_):
        new_class = type.__new__(cls, name, bases, dict_)

        if '__metaclass__' in dict_ and dict_['__metaclass__'] == FinderType:
            new_class.child_classes = {}
        elif hasattr(new_class, 'application_id'):
            new_class.child_classes[name] = new_class

            cls.prepare_new_class(new_class)

        return new_class

    def prepare_new_class(cls):
        try:
            cls.app_icon = alfred.Icon()
            cls.app_name, \
            cls.app_icon.iconpath = query_application_id_for_name_and_icon(cls.application_id)
        except ValueError:
            cls.is_available = False
        else:
            cls.is_available = True


class BaseFinder(object):

    __metaclass__ = FinderType

    _user_preferences_path = path.expanduser('~/Library/Preferences')

    def get_preferences_file(self, *args):
        return path.join(self._user_preferences_path, *args)

    def find_items(self, query):
        raise NotImplementedError

    def open(self, project_path):
        subprocess.call(['open', '-b',  self.application_id, project_path])

    @property
    def uid(self):
        return self.__module__.rsplit('.', 1)[-1:][0]

    @property
    def path(self):
        return path.abspath(
            self.__module__.replace('.', '/')
        )

    def icon_for_path(self, path):
        return self.app_icon

    def create_item(self, name, path):
        return alfred.Item(
            uid='%s:%s' % (self.uid, name),
            arg='%s %s' % (self.uid, path),
            autocomplete=name,
            title=name,
            subtitle=path,
            icon=self.icon_for_path(path)
        )

    @property
    def filter_item(self):
        return alfred.Item(
            uid=self.uid,
            arg=self.uid,
            autocomplete=self.uid + ' ',
            valid=False,
            title=self.app_name,
            icon=self.app_icon
        )