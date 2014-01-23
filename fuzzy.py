import re

class FuzzyMatcher(object):

    DEFAULT_THRESHOLD = 0.1

    pattern = ''

    def __init__(self, pattern=''):
        self.setPattern(pattern)

    def setPattern(self, pattern):
        self.pattern = '.*?'.join(map(re.escape, list(pattern)))

    def score(self, string):
        match = re.search(self.pattern, string)
        if match is None:
            return 0
        else:
            return min(1.0 / ((1 + match.start()) * (match.end() - match.start() + 1)), 1.0)

    def filter_iterator(self, items, key=lambda k: k, threshold=DEFAULT_THRESHOLD):
        for item in items:
            if self.score(key(item)) > threshold:
                yield item

    def filter(self, items, key=lambda k: k, threshold=DEFAULT_THRESHOLD):
        return [i for i in self.filter_iterator(items, key, threshold)]

if __name__ == '__main__':
    import sys

    fuzzy = FuzzyMatcher(sys.argv[1])

    print fuzzy.filter(sys.argv[2:])


