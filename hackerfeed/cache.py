import hashlib
import json
import os


class Cache(object):
    ENTRIES_SUFFIX = '.list'
    METADATA_SUFFIX = '.json'

    def __init__(self, cache_dir):
        self.__cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def __open(self, key, suffix, mode='r'):
        h = hashlib.sha1()
        h.update(key.encode('utf-8'))
        real_path = os.path.join(self.__cache_dir, '%s%s' % (h.hexdigest(), suffix))

        return open(real_path, mode)

    def set_metadata(self, key, json_data):
        fd = self.__open(key, self.METADATA_SUFFIX, 'w')
        json.dump(json_data, fd)
        fd.write("\n")

    def get_metadata(self, key):
        try:
            return json.load(self.__open(key, self.METADATA_SUFFIX, 'r'))
        except FileNotFoundError:
            return {}

    def set_entry_list(self, key, entries):
        fd = self.__open(key, self.ENTRIES_SUFFIX, 'w')
        for entry in sorted(entries, key=lambda x: x['updated'], reverse=True):
            json.dump(entry, fd)
            fd.write("\n")

    def get_entry_list(self, key):
        fd = self.__open(key, self.ENTRIES_SUFFIX, 'r')
        return (json.loads(line) for line in fd)
