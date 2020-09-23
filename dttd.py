import os
import time
import stat


class DTTD():
    def __init__(self, directories="directories", files="files"):
        self.DIRECTORIES = directories
        self.FILES = files

    def __deep_insert(self, keys, dictionary, value):
        key = keys[0]
        if len(keys) == 1:
            if isinstance(dictionary, list):
                for i in range(len(dictionary)):
                    if [*dictionary[i]][0] == key:
                        dictionary[i][key] = value
            else:
                dictionary[key] = value
        elif isinstance(dictionary, list):
            for i in range(len(dictionary)):
                if [*dictionary[i]][0] == key:
                    dictionary[i][key] = self.__deep_insert(keys[1:], dictionary[i][key], value)
        else:
            dictionary[key] = self.__deep_insert(keys[1:], dictionary[key], value)
        return dictionary

    def __add_directories_to_dir(self, dir, dirs, index_path):
        value = {
            self.DIRECTORIES: [{i: {}} for i in sorted( dirs )],
        }
        self.__deep_insert(index_path, dir, value)

    def __add_files_to_dir(self, dir, files, index_path, path, filtered_file_ext):
        if filtered_file_ext:
            files = filter(lambda x: any(e in x for e in filtered_file_ext), files)
        value = []
        for f in sorted(files):
            file_path = path + "/" + f
            file_stats = os.stat(file_path)
            file_dict = {
                f: {
                    "path": file_path,
                    "accessed": time.ctime( file_stats[ stat.ST_ATIME ] )
                }
            }
            value.append(file_dict)
        self.__deep_insert(index_path, dir, {self.FILES: value})


    def get_directory_structure(self,rootdir, filtered_file_ext=None):
        dir = {}
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            index_path = self.create_index_path(path, start)
            if len(dirs):
                self.__add_directories_to_dir(dir, dirs, index_path)
            if len(files):
                self.__add_files_to_dir(dir, files, index_path, path, filtered_file_ext)
        return dir

    def create_index_path(self, path, start):
            folders = path[start:].split(os.sep)
            index_path = []
            for f in folders:
                index_path.append(f)
                index_path.append(self.DIRECTORIES)
            return index_path[0:-1]


