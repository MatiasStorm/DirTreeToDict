from ..dttd import DTTD
import pytest

@pytest.fixture(scope="session")
def empty_directory(tmpdir_factory):
    folder = tmpdir_factory.mktemp("folder1")
    return folder

@pytest.fixture(scope="session")
def nested_directories(tmpdir_factory):
    folder = tmpdir_factory.mktemp("nested_folder")
    for i in range(3):
        sub_folder = folder.mkdir(f"sub_folder{i}")
        for j in range(3):
            sub_folder.mkdir(f"subsub_folder{j}")
    return folder

@pytest.fixture(scope="session")
def nested_dirs_w_files(tmpdir_factory):
    folder = tmpdir_factory.mktemp("nested_file_folder")
    for i in range(2):
        sub_folder = folder.mkdir(f"sub_folder{i}")
        for j in range(2):
            sub_sub_folder = sub_folder.mkdir(f"subsub_folder{j}").join(f"file{j}.txt")
    return folder


class TestDTTD():
    def test_one(self, empty_directory):
        dttd = DTTD()
        actual = dttd.get_directory_structure(str(empty_directory))
        expected = {}
        assert actual == expected

    def test_nested_directory(self, nested_directories):
        dttd = DTTD()
        actual = dttd.get_directory_structure(str(nested_directories))
        expected = {
            'nested_folder0': {
                'directories': [
                    {
                        'sub_folder0': {
                            'directories': [
                                {'subsub_folder0': {}},
                                {'subsub_folder1': {}},
                                {'subsub_folder2': {}}
                            ]
                        }
                    },
                    {
                        'sub_folder1': {
                            'directories': [
                                {'subsub_folder0': {}},
                                {'subsub_folder1': {}},
                                {'subsub_folder2': {}}
                            ]
                        }
                    },
                    {
                        'sub_folder2': {
                            'directories': [
                                {'subsub_folder0': {}},
                                {'subsub_folder1': {}},
                                {'subsub_folder2': {}}
                            ]
                        }
                    }
                ]
            }
        }
        assert actual == expected

    def test_dested_dirs_w_files(self, nested_dirs_w_files):
        dttd = DTTD()
        actual = dttd.get_directory_structure(str(nested_dirs_w_files))

