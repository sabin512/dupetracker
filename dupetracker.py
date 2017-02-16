from collections import defaultdict
from pathlib import Path
from datetime import datetime

from dupeutils import get_file_hash
from dupeutils import NullOutput

class DupeTracker():
    def __init__(self,suffix=None, output=NullOutput()):
        self.dupe_map = defaultdict(list)
        self.suffix = suffix
        self.output = output

    def map_file(self, file_to_map):
        if self.suffix and file_to_map.suffix.lower() != self.suffix.lower():
            return

        self.output.show_verbose_message('Scanning file ' + file_to_map.as_posix())

        file_hash = get_file_hash(file_to_map.as_posix())
        self.dupe_map[file_hash].append(file_to_map.as_posix())

    def scan_dir(self, directory=None, root=True):
        path = Path(directory) if directory else Path.cwd()

        if root:
            self.output.show_message('Scanning %s for duplicate %s files' % (path.as_posix(), self.suffix))
            #this part is silly, if there's ever a GUI we probably wouldn't rely on a keyboard interrupt
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
            self.output.show_message('\nScanning %s took %s seconds' % (path.as_posix(), elapsed_seconds))

    def trim_dupe_map(self):
        self.output.show_message('Cleaning up file map with %s hashes' % len(self.dupe_map))
        single_hashes = []
        for file_hash in self.dupe_map:
            if len(self.dupe_map[file_hash]) == 1:
                single_hashes.append(file_hash)

        for single_hash in single_hashes:
            del self.dupe_map[single_hash]

        self.output.show_message('File map now has %s hashes' % len(self.dupe_map))
