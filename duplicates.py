import os
import sys
import operator
from collections import Counter


def get_duplicates(list_of_files):
    inodes = []
    file_infos = {}

    for filename in list_of_files:
        if not os.path.isfile(filename):
            continue
        info = os.stat(filename)
        # If files have the same inodes - they are not duplicated
        if info.st_ino not in inodes:
            inodes.append(info.st_ino)
            file_infos[filename] = info

    counter = Counter(map(lambda x: x.st_size, file_infos.values()))
    not_unique_sizes = [key for key, value in counter.items() if value > 1]

    # duplicates is key-value store with:
    # - key as size of duplicates
    # - value as list of filenames of duplicates
    duplicates = {}
    for size in not_unique_sizes:
        duplicates[size] = []
        for filename, file_info in file_infos.items():
            if file_info.st_size == size:
                duplicates[size].append(filename)

    return duplicates


def print_duplicates(duplicates):
    for size, filenames in duplicates.items():
        print('\nFollowing files are duplicated with size {}:'.format(size))
        for filename in filenames:
            print(filename)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = '.'

    files_list = []
    for root, dirs, files in os.walk(folder):
        files_list.extend([(root, filename) for filename in files])

    all_filenames = map(operator.itemgetter(1), files_list)
    counter = Counter(all_filenames)
    not_unique_filenames = [key for key, value in counter.items() if value > 1]

    for filename in not_unique_filenames:
        filenames = ['{}/{}'.format(path, name) for path, name in files_list if name == filename]
        duplicates = get_duplicates(filenames)
        if duplicates:
            print('Found duplicated files with filename "{}"'.format(filename))
            print_duplicates(duplicates)
            print('*' * 79)
