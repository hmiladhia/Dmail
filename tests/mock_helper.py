import re


class String:
    """A helper object that compares strings to a regex pattern"""
    def __init__(self, pattern, flags=0):
        self.pattern = pattern
        self.flags = flags

    def __eq__(self, other):
        return re.fullmatch(self.pattern, other, self.flags) is not None

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f'<String({self.pattern} ,{self.flags})>'
