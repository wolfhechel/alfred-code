import pkgutil

from ._base import BaseFinder

finders = pkgutil.walk_packages(
    path = __path__,
    prefix= __name__ + '.',
    onerror=lambda e: None
)

for module_loader, name, ispkg in finders:
    if not name.endswith('_base'):
        __import__(name)

def get_available_finders():
    return [c() for c in BaseFinder.child_classes.values() if c.is_available()]

def get_finder(finder_uid):
    available_finders = get_available_finders()

    for finder in available_finders:
        if finder.uid == finder_uid:
            return finder