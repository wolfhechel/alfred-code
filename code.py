#!/usr/bin/env python2.7
import workflow

def get_ignored_items(wf):
    return wf.stored_data('ignored_items') or []

def set_ignored_items(wf, ignored_items):
    wf.store_data('ignored_items', ignored_items)

def query(finders, query, wf):
    items = []

    ignored_items = get_ignored_items(wf)

    for finder in finders:
        items.extend([d for d in finder.find_items() if d['arg'] not in ignored_items])

    if query:
        items = wf.filter(query, items, lambda i: i['title'])

    for item in items:
        wf.add_item(**item)

    return True

def open(finders, query, wf):
    finder_uid, project_path = query.split(' ', 1)

    def get_finder(finder_uid):
        for finder in finders:
            if finder.uid == finder_uid:
                return finder

    finder = get_finder(finder_uid)

    if finder:
        finder.open(project_path)

def ignore(finders, query, wf):
    escaped_query = query.replace('\\', '')

    ignored_items = get_ignored_items(wf)

    if escaped_query not in ignored_items:
        ignored_items.append(escaped_query)

    set_ignored_items(wf, ignored_items)

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    action = parser.add_mutually_exclusive_group(required=True)

    action.add_argument('--query', dest='action', action='store_const',
                        const=query)

    action.add_argument('--open', dest='action', action='store_const',
                        const=open)

    action.add_argument('--ignore', dest='action', action='store_const',
                        const=ignore)

    parser.add_argument('query', nargs='?', default='', type=unicode)

    args = parser.parse_args()

    def wf_func(wf):
        import finders

        available_finders = finders.get_available_finders(wf)

        feedback = args.action(available_finders, args.query, wf)

        if isinstance(feedback, basestring):
            print feedback
        elif feedback:
            wf.send_feedback()

    wf = workflow.Workflow()

    sys.exit(wf.run(wf_func))