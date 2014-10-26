#!/usr/bin/env python2.7
import workflow

def query(finders, query, wf):
    items = []

    for finder in finders:
        items.extend(finder.find_items())

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

    return False

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()

    action = parser.add_mutually_exclusive_group(required=True)

    action.add_argument('--query', dest='action', action='store_const',
                        const=query)

    action.add_argument('--open', dest='action', action='store_const',
                        const=open)

    parser.add_argument('query', nargs='?', default='', type=unicode)

    args = parser.parse_args()

    def wf_func(wf):
        import finders

        available_finders = finders.get_available_finders(wf)

        if args.action(available_finders, args.query, wf):
            wf.send_feedback()

    wf = workflow.Workflow()

    sys.exit(wf.run(wf_func))