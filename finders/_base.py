import alfred
from os import path


class FinderType(type):
    def __new__(cls, name, bases, dict_):
        new_class = type.__new__(cls, name, bases, dict_)

        if '__metaclass__' in dict_ and dict_['__metaclass__'] == FinderType:
            new_class.child_classes = {}
        else:
            new_class.child_classes[name] = new_class

        return new_class



class BaseFinder(object):

    __metaclass__ = FinderType

    @staticmethod
    def is_available():
        raise NotImplementedError

    def find_items(self, query):
        raise NotImplementedError

    @property
    def uid(self):
        return self.__module__.rsplit('.', 1)[-1:][0]

    @property
    def path(self):
        return path.abspath(
            self.__module__.replace('.', '/')
        )

    def create_item(self, name, path):
        return alfred.Item(
            uid='%s:%s' % (self.uid, name),
            arg='%s %s' % (self.application, path),
            autocomplete=name,
            title=name,
            subtitle=path,
            icon='%s/icon.png' % self.path
        )

    @property
    def filter_item(self):
        return alfred.Item(
            uid=self.uid,
            arg=self.uid,
            autocomplete=self.uid + ' ',
            valid=False,
            title=self.uid,
            icon='%s/icon.png' % self.path
        )