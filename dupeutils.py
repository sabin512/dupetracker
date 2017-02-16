import hashlib

class NullOutput():
    def show_message(self, message):
        pass
    def show_verbose_message(self, message):
        pass
    def update_progress(self):
        pass
            
BLOCKSIZE = 65536
def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest()
