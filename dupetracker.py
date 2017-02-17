"""
This module holds the DupeTracker class.
Instances of this class can be used to scan directories for duplicate files.
The class relies on a dictionary keyed by unique file hashes which
holds lists of the files sharing each hash.
"""
from collections import defaultdict
from pathlib import Path
from datetime import datetime

from dupeutils import get_file_hash
from dupeutils import NullOutput

class DupeTracker():
    """
    This class builds and manages a dictionary of files grouped by unique hashes.
    The dupe_map within allows the user to determine duplicate files by checking which
    keys point to more than one file.
    """
    def __init__(self, suffix=None, output=NullOutput()):
        self.dupe_map = defaultdict(list)
        self.suffix = suffix
        self.output = output

    def map_file(self, file_to_map):
        """
        Generates a has for a file and adds the file name to the appropriate list in the dupe_map.
        Only files with a given suffix (file extension) are mapped if such a suffix was configured.
        """
        if self.suffix and file_to_map.suffix.lower() != self.suffix.lower():
            return

        self.output.show_verbose_message('Scanning file ' + file_to_map.as_posix())

        file_hash = get_file_hash(file_to_map.as_posix())
        self.dupe_map[file_hash].append(file_to_map.as_posix())

    def scan_dir(self, directory=None, root=True):
        """
        Scan a directory and its subdirectories for duplicates and map the files as needed.

        Keyword arguments:
        directory -- the directory to scan, if this is absent, the current directory will be used.
        root      -- this is True if we are at the root of the scan,
                     it will be False when recursion begins.

        """
        path = Path(directory) if directory else Path.cwd()

        if root:
            self.output.show_message('Scanning %s for duplicate %s files' % (path.as_posix(),
                                                                             self.suffix))
            #this part is silly, if there's ever a GUI we probably
            #wouldn't rely on a keyboard interrupt
            self.output.show_message('Press Control+C to cancel')
            start_time = datetime.now()

        for child in path.iterdir():
            if child.is_dir():
                self.scan_dir(child, root=False)
            else:
                self.map_file(child)

        self.output.update_progress()

        if root:
            elapsed_seconds = (datetime.now() - start_time).total_seconds()
            self.output.show_message('\nScanning %s took %s seconds' % (path.as_posix(),
                                                                        elapsed_seconds))

    def trim_dupe_map(self):
        """
        This method can be used to trim entries from the dupe_map which only point to one file.
        """
        self.output.show_message('Cleaning up file map with %s hashes' % len(self.dupe_map))
        single_hashes = []
        for file_hash in self.dupe_map:
            if len(self.dupe_map[file_hash]) == 1:
                single_hashes.append(file_hash)

        for single_hash in single_hashes:
            del self.dupe_map[single_hash]

        self.output.show_message('File map now has %s hashes' % len(self.dupe_map))
