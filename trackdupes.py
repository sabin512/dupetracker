#!/usr/bin/python3
import argparse
import sys

from dupeutils import NullOutput
from dupetracker import DupeTracker

def print_dupe_report(dupe_map, output=NullOutput()):
    output.show_message('The following duplicate files have been found:')
    
    for file_hash, dupe_list in dupe_map.items():
        if len(dupe_list) == 1:
            continue
        output.show_message('\nHash %s is repeated in:' % file_hash)
        output.show_message('    ' + '\n    '.join(dupe_list))

#this could probably be logger, but the dream is that one day all this is redirected into a GUI
class ConsoleOutput():
    def __init__(self, verbose=None):
        self.verbose = verbose

    def show_message(self, message):
        print(message)

    def show_verbose_message(self, message):
        if self.verbose:
            print(message)

    def update_progress(self):
        if not self.verbose:
            print('.', end='', flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--extension', help='Extension to scan for')
    parser.add_argument('-d', '--directory', help='Root of the directories to scan')
    parser.add_argument('-v', '--verbose', 
                        action='store_true', help='List all the files being scanned')
    args = parser.parse_args()
    
    output = ConsoleOutput(args.verbose)
    tracker = DupeTracker(args.extension, output)
    tracker.scan_dir(args.directory)
    print()
    #tracker.trim_dupe_map()
    print_dupe_report(tracker.dupe_map, output)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nTracking cancelled by user')
        sys.exit(0)
