#!/usr/bin/python3
import sys
import hashlib
from pathlib import Path
from datetime import datetime 
import argparse

BLOCKSIZE = 65536
def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()


class DupeTracker():
    def __init__(self,suffix=None):
        self.file_map = {}
        self.suffix = suffix

    def map_file(self, file_to_map):
        if self.suffix and file_to_map.suffix.lower() != self.suffix.lower():
            return
        #print('Mapping file ' + file_to_map.as_posix())
        file_hash = get_file_hash(file_to_map.as_posix())
        if file_hash in self.file_map:
            self.file_map[file_hash].append(file_to_map.as_posix())
        else:
            self.file_map[file_hash] = [file_to_map.as_posix()]

    def scan_dir(self, directory=None, root=True):
        path = Path(directory) if directory else Path.cwd()

        if root:
            print('Scanning %s for duplicate %s files' % (path.as_posix(), self.suffix))
            print('Press Control+C to cancel')
            start_time = datetime.now()

        for child in path.iterdir():
            if child.is_dir():
                self.scan_dir(child, root=False)
            else:
                self.map_file(child)
        print('.', end='',flush=True)

        if root:
            elapsed_seconds = (datetime.now() - start_time).total_seconds()
            print('\nScanning %s took %s seconds' % (path.as_posix(), elapsed_seconds))

    def trim_file_map(self):
        print('Cleaning up file map with %s hashes' % len(self.file_map))
        single_hashes = []
        for file_hash in self.file_map:
            if len(self.file_map[file_hash]) == 1:
                single_hashes.append(file_hash)

        for single_hash in single_hashes:
            del self.file_map[single_hash]

        # list comprehensions seem fancier, yet I still find they impact readability
        #[single_hashes.append(file_hash) for file_hash in file_map if len(file_map[file_hash]) == 1]
        #[del file_map[single_hash] for single_hash in single_hashes]

        print('File map now has %s hashes' % len(self.file_map))

    def print_dupe_report(self):
        print('The following duplicate files have been found:')
        for file_hash in self.file_map:
            if len(self.file_map[file_hash]) == 1:
                continue
            print('\nHash %s is repeated in:' % file_hash)
            print('    ' + '\n    '.join(self.file_map[file_hash]))
            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--extension', help='Extension to scan for')
    parser.add_argument('-d', '--directory', help='Root of the directories to scan')
    args = parser.parse_args()
    
    directory = None
    extension  = None

    if args.directory:
        directory = args.directory
    if args.extension:
        extension = args.extension

    tracker = DupeTracker(extension)
    tracker.scan_dir(directory)
    print()
    #tracker.trim_file_map()
    tracker.print_dupe_report()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nTracking cancelled by user')
        sys.exit(0)
