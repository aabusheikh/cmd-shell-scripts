#!/bin/python3

from os import path, listdir, remove
from shutil import rmtree
import sys


WGET_FTP_LISTING_FILE_NAME = ".listing"
WGET_FTP_LISTING_N_SPLITS = 8


def get_wget_ftp_listing_items(root_path):
    if not path.isdir(root_path):
        print(f"{root_path} is not a valid directory path")
        return None

    listing_file_path = path.join(root_path, WGET_FTP_LISTING_FILE_NAME)
    if not path.isfile(listing_file_path):
        print(f"Can't find file {listing_file_path}")
        return None
    
    try:
        with open(listing_file_path) as listing_file:
            listing_lines = [line.rstrip('\n') for line in listing_file]
        listing_items = [line.split(maxsplit=WGET_FTP_LISTING_N_SPLITS)[-1] for line in listing_lines]
    except:
        print(f"Can't read or parse file {listing_file_path}")
        return None

    try:
        listing_items.append(WGET_FTP_LISTING_FILE_NAME)
        listing_items.remove('.')
        listing_items.remove('..')
    except:
        print("Error while adding .listing and removing . and ..")
        return None

    return listing_items


def wget_mirror_ftp_cleanup(root_path):
    if not path.isdir(root_path):
        print(f"{root_path} is not a valid directory path")
    else:
        listing_items = get_wget_ftp_listing_items(root_path)
        if listing_items is None:
            print("Failed to read listing items from .listing file")
        else:
            for dir_item in listdir(root_path):
                delete_item = dir_item not in listing_items
                item_path = path.join(root_path, dir_item)
                if path.isdir(item_path):
                    if delete_item:
                        print(f"Removing directory {item_path}")
                        rmtree(item_path)
                    else:
                        wget_mirror_ftp_cleanup(item_path)
                elif path.isfile(item_path):
                    if delete_item:
                        print(f"Removing file {item_path}")
                        remove(item_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide a valid directory path")
    else:
        root_path = path.abspath(sys.argv[1])
        if not path.isdir(root_path):
            print(f"{root_path} is not a valid directory path")
        else:
            wget_mirror_ftp_cleanup(root_path)