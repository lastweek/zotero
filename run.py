#!/usr/bin/env python3

import operator
import sys
from pyzotero import zotero

library_id=6048482
library_type='user'

# This key has read access
api_key='zpi8IRsEUQn9FjLcO4AwwwLh'

#
# This API call will dump all the item names under a collection
# Default to a csv format.
#
def dumpItemsOfCollection(zot, col):
    collectionID=col['data']['key']
    items = zot.everything(zot.collection_items(collectionID))
    for item in items:
        if item['data']['itemType'] != "attachment":
            pub = 'unknown'
            if item['data']['itemType'] == 'journalArticle':
                pub = item['data']['publicationTitle']
            if item['data']['itemType'] == 'conferencePaper':
                pub = item['data']['proceedingsTitle']

            #  print(item)
            print("%s,%s,%s" %(item['data']['title'], item['data']['date'], pub))

#
# This function is used to update all item's type, publication title, and year
# I use this after I add all papers from a conference. Serve as a batch operation.
#
def updateItemsOfCollection(zot, col, publication, year):
    collectionID=col['data']['key']
    items = zot.everything(zot.collection_items(collectionID))
    for item in items:
        if item['data']['itemType'] != "attachment":
            item['data']['itemType'] = 'conferencePaper'
            item['data']['date'] = year
            item['data']['proceedingsTitle'] = publication
            zot.update_item(item)

def findCollectionByName(zot, name):
    cols = zot.everything(zot.collections())
    for col in cols:
        if col['data']['name'] == name:
            return col
    return None

def dumpCollectionRecursive(zot, col, i, recursive):
    spacing=' '*i
    print("%s- %s" % (spacing, col['data']['name']))

    if recursive == True:
        sub = zot.everything(zot.collections_sub(col['data']['key']))
        sub = sorted(sub, key=lambda i:i['data']['name'])
        for s in sub:
            dumpCollectionRecursive(zot, s, i+4, recursive)

#
# Print all directories recursively
#
def dumpAllCollections(zot):
    cols = zot.everything(zot.collections_top())
    cols = sorted(cols, key=lambda i:i['data']['name'])
    recursive = True
    for col in cols:
        dumpCollectionRecursive(zot, col, 0, recursive=recursive)

def main():

    zot = zotero.Zotero(library_id, library_type, api_key)
    print("Please enable scripts as needed..")

    #
    # This section is used to update proceedings
    #
    #  col = findCollectionByName("07-ATC21")
    #  if col != None:
    #      updateItemsOfCollection(col, "ATC", "2021")
    #      dumpItemsOfCollection(col)
    #  col = findCollectionByName("07-OSDI21")
    #  if col != None:
    #      updateItemsOfCollection(col, "OSDI", "2021")
    #      dumpItemsOfCollection(col)
    #  col = findCollectionByName("08-SIGCOMM21")
    #  if col != None:
    #      updateItemsOfCollection(col, "SIGCOMM", "2021")
    #      dumpItemsOfCollection(col)

    dumpAllCollections(zot)

    print("All Done!")

if __name__ == "__main__":
    main()
