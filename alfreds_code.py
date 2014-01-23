import subprocess
from alfred import render
from fuzzy import FuzzyMatcher

import finders

def filter_items(items, query):
    fuzzy = FuzzyMatcher(query)

    return fuzzy.filter(items, key=lambda x: x.title.lower())

def lookup(query):
    query = query.strip().lower()

    items = []

    available_finders = finders.get_available_finders()

    if query:
        if ' ' in query:
            finder_uid, query = query.split(' ', 1)
        else:
            finder_uid = query

        finder = finders.get_finder(finder_uid)

        if finder:
            available_finders = [finder]

            if finder_uid == query:
                query = ''
        else:
            for finder in available_finders:
                items.append(finder.filter_item)

        for finder in available_finders:
            assert isinstance(finder, finders.BaseFinder)

            items.extend(finder.find_items(query))

        items = filter_items(items, query)
    else:
        for finder in available_finders:
            items.append(finder.filter_item)



    return render(items)

def open(query):
    finder_uid, project_path = query.split(' ', 1)

    finder = finders.get_finder(finder_uid)

    return subprocess.call(['open', '-a',  finder.application, project_path])

if __name__ == '__main__':
    import sys

    query = ' '.join(sys.argv[1:])
    print query

    print open(query)