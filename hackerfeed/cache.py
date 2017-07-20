import hashlib
import json
import os


class Cache(object):
    def __init__(self, cache_dir):
        self.__cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def __open(self, key, mode='r'):
        h = hashlib.sha1()
        h.update(key.encode('utf-8'))
        real_path = os.path.join(self.__cache_dir, h.hexdigest() + '.json')

        return open(real_path, mode)

    def set_json(self, key, json_data):
        json.dump(json_data, self.__open(key, 'w'))

    def get_json(self, key):
        return json.load(self.__open(key, 'r'))

    def set_entry_list(self, key, entries):
        fd = self.__open(key, 'w')
        for entry in sorted(entries, key=lambda x: x['updated'], reverse=True):
            json.dump(entry, fd)
            fd.write("\n")

    def get_entry_list(self, key):
        fd = self.__open(key, 'r')
        return (json.loads(line) for line in fd)
