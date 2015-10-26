# coding: utf-8

import csv
import re

# constants
po_file_pass = 'Japanese/Japanese.po'
csv_file_pass = 'Japanese.csv'

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

dict_po = dict()  # {text_id:(English, Japanese)}


def read_po(po_file_pass=po_file_pass, target_dict=dict_po):
    pass


def read_csv(csv_file_pass=csv_file_pass, target_dict=dict_po):
    pass


def po_to_csv(po_file_pass=po_file_pass, csv_file_pass=csv_file_pass):
    pass


def csv_to_po(csv_file_pass=csv_file_pass, po_file_pass=po_file_pass):
    pass


if __name__ == '__main__':
    pass
