#!/usr/bin/env python3

import operator
import sys
from pyzotero import zotero

library_id=6048482
library_type='user'
api_key='zpi8IRsEUQn9FjLcO4AwwwLh'
zot = zotero.Zotero(library_id, library_type, api_key)

items = zot.top(limit=1)
# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for item in items:
    #  print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))
    print(item)
    collectionId = item['data']['collections']
    print('Title: %s | Date: %s | Collection: %s' %
            (item['data']['title'], item['data']['date'], collectionId))

#  items = zot.collection_items('ZLYZXXRN')
#  for item in items:
#      print('\n Title: %s | DateAdded: %s | Tags: %s' % (item['data']['title'], item['data']['dateAdded'], item['data']['tags']))


def printDir(col, i):
    spacing=' '*i
    print("%s%s" % (spacing, col['data']['name']))
    #  sub = zot.collections_sub(col['data']['key'])
    #  for s in sub:
    #      printDir(s, i+2)

cols = zot.everything(zot.collections_top())
print(cols)
sorted(cols, key=lambda x: x['data']['name'])
for col in cols:
    printDir(col, 0)
