# coding: utf-8

import csv
import re

# constants
po_file_pass = 'Japanese/japanese.po'
csv_file_pass = 'japanese.csv'

comment = '#:'
msgctxt = 'msgctxt'
msgid = 'msgid'
msgstr = 'msgstr'

entry = """
^\#: ([.\w]+)$          # comment. same as msgctxt
^msgctxt "([.\w]+)"$    # text id
^msgid "(.*)"$          # original text
^msgstr "(.*)"$         # translated text
"""

regex_entry = re.compile(entry, re.VERBOSE)


if __name__ == '__main__':
    pass