import re


class RegexEqual(str):
    def __eq__(self, pattern):
        return bool(re.search(pattern, self))
