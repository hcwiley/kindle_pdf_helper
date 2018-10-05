#!/usr/bin/env python

'''
usage:   unspread.py my.pdf

Creates unspread.my.pdf

Chops each page in half, e.g. if a source were
created in booklet form, you could extract individual
pages.
'''

import sys
import os
import argparse

from pdfrw import PdfReader, PdfWriter, PageMerge


def splitpage(src):
  ''' Split a page into two (left and right)
  '''
  # Yield a result for each half of the page
  for x_pos in (0, 0.5):
    yield PageMerge().add(src, viewrect=(x_pos, 0, 0.5, 1)).render()


parser = argparse.ArgumentParser(description='Configure which how to unspread.')
parser.add_argument('--skip_first', dest='skip_first', action='store_true',
                    default=False,
                    help='skip the first page')
parser.add_argument('--skip_last', dest='skip_last', action='store_true',
                    default=False,
                    help='skip the last page')
parser.add_argument('--only_pages', dest='only_pages', nargs='+',
                    help='only unspread these pages')
parser.add_argument("path", help="path of the PDF to unspread")

args = parser.parse_args()
if args.only_pages:
  args.only_pages = args.only_pages[0].split(',')
print args

inpfn = args.path
outfn = 'unspread.' + os.path.basename(inpfn)
writer = PdfWriter(outfn)

pageIdx = -1
all_the_pages = PdfReader(inpfn).pages
for page in all_the_pages:
  pageIdx += 1
  if pageIdx == 0 and args.skip_first:
    print('skip first')
    continue
  if pageIdx == len(all_the_pages) and args.skip_last:
    print('skip last')
    continue
  if args.only_pages and not str(pageIdx) in args.only_pages:
    print('skipping {}'.format(pageIdx))
    continue
  writer.addpages(splitpage(page))
writer.write()
