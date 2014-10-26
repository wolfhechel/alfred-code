import pkgutil
import AppKit

from ._base import BaseFinder

finders = pkgutil.walk_packages(
    path = __path__,
    prefix= __name__ + '.',
    onerror=lambda e: None
)

for module_loader, name, ispkg in finders:
    if not name.endswith('_base'):
        __import__(name)

workspace = AppKit.NSWorkspace.sharedWorkspace()

def get_available_finders(wf):
    return [c(wf) for c in BaseFinder.child_classes.values() if c.is_available]