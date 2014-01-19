from difflib import SequenceMatcher
import subprocess
from alfred import render

import finders

def filter_items(items, query):
    if not query:
        return items

    ratio = 0.35

    sequence_matcher = SequenceMatcher()
    sequence_matcher.set_seq2(query.lower())

    matched_items = {}

    for item in items:
        sequence_matcher.set_seq1(item.title.lower())

        match_ratio = sequence_matcher.ratio()

        if match_ratio >= ratio:
            matched_items[item] = match_ratio

    return sorted(
        matched_items.keys(),
        key=lambda i: -matched_items[i]
    )


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

        for finder in available_finders:
            assert isinstance(finder, finders.BaseFinder)

            items.extend(finder.find_items(query))

        items = filter_items(items, query)

    else:
        for finder in available_finders:
            items.append(finder.filter_item)

    return render(items)

def open(query):
    application, project_path = query.split(' ', 1)

    return subprocess.call(['open', '-a',  application, project_path])

if __name__ == '__main__':
    import sys

    print lookup(' '.join(sys.argv[1:]))