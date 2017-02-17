#!/usr/bin/python3
"""
This is a command line interface for a small utility which finds duplicate files.
By default the current directory will be scanned for any types of files,
however the user may choose to scan a specific directory for specific file extensions.
"""
import argparse
import sys

from dupeutils import NullOutput
from dupetracker import DupeTracker

def print_dupe_report(dupe_map, output=NullOutput()):
    """
    This prints a somewhat formatted report of the duplicates found to standard out.
    """
    output.show_message('The following duplicate files have been found:')

    for file_hash, dupe_list in dupe_map.items():
        if len(dupe_list) == 1:
            continue
        output.show_message('\nHash %s is repeated in:' % file_hash)
        output.show_message('    ' + '\n    '.join(dupe_list))

#this could probably be logger, but the dream is that one day all this is redirected into a GUI
class ConsoleOutput():
    """
    This class shows messages to standard out according to the interface needed by DupeTracker.
    """
    def __init__(self, verbose=None):
        self.verbose = verbose

    def show_message(self, message):
        """
        Print a regular message to standard out.
        """
        print(message)

    def show_verbose_message(self, message):
        """
        Print a verbose message to standard out.
        """
        if self.verbose:
            print(message)

    def update_progress(self):
        """
        Prints dots to standard out on a single line as the file scanning advances.
        """
        if not self.verbose:
            print('.', end='', flush=True)

def main():
    """
    Main function you silly lint.
    """
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
