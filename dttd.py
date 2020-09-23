import os
import time
import stat


class DTTD():
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

    def get_directory_structure(self,rootdir, filtered_file_ext=None):
        DIRECTORIES = "directories"
        FILES = "files"
        dir = {}
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            dict_path = []
            for f in folders:
                dict_path.append(f)
                dict_path.append(DIRECTORIES)
            dict_path = dict_path[0:-1]

            if len(dirs):
                value = {
                    DIRECTORIES: [{i: {}} for i in sorted( dirs )],
                }
                self.__deep_insert(dict_path, dir, value)

            if len(files):
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
                self.__deep_insert(dict_path, dir, {FILES: value})
        return dir

