"""
Utility code for DupeTracker.
"""
import hashlib

class NullOutput():
    """
    Default output class for DupeTracker.
    This will suppress DupeTracker messages.
    """
    def show_message(self, message):
        """
        Empty implementation.
        """
        pass
    def show_verbose_message(self, message):
        """
        Empty implementation.
        """
        pass
    def update_progress(self):
        """
        Empty implementation.
        """
        pass

BLOCKSIZE = 65536
def get_file_hash(file_path):
    """
    Generate a SHA-256 has for a given file.
    """
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file_to_scan:
        buf = file_to_scan.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file_to_scan.read(BLOCKSIZE)
    return hasher.hexdigest()
