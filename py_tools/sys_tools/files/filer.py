import os
import fnmatch
import shutil
from pathlib import Path
from datetime import datetime


# Locating group

def list_dir(folder):
    """
    List files in a folder

    :param folder: folder to scan
    :return: None
    """
    with open('list_dir.txt', 'w') as f:
        for file_name in os.listdir(folder):
            f.write(file_name + '\n')
            print(file_name)


def ends_with(folder: str, search: str) -> None:
    """
    List files in a folder that end with a specific string

    :param folder: str folder to scan
    :param search: str string to search for
    :return: None
    """
    for file_name in os.listdir(folder):
        if file_name.endswith(search):
            print(file_name)


def starts_with(folder: str, search: str) -> None:
    """
    List files in a folder that start with a specific string

    :param folder: str folder to scan
    :param search: str string to search for
    :return: None
    """
    for file_name in os.listdir(folder):
        if file_name.startswith(search):
            print(file_name)


def file_name_match(folder: str, search: str) -> None:
    """
    List files in a folder that match a specific string

    :param folder: str folder to scan
    :param search: str string to search for
    :return: None
    """
    for file_name in os.listdir(folder):
        if fnmatch.fnmatch(file_name, search):
            print(file_name)


def glob_match(folder: str, search: str) -> None:
    """
    List files in a folder that match a specific string

    :param folder: str folder to scan
    :param search: str string to search for
    :return: None
    """
    p = Path(folder)
    n: Path
    for n in p.glob(search):
        print(n)


# Manipulating group

def get_date(time_stamp: float) -> str:
    """
    Get date from time stamp in seconds since the epoch

    :param time_stamp: float time stamp in seconds since the epoch
    :return: str date in format 'dd mmm yyyy'
    """
    # return datetime.utcfromtimestamp(time_stamp).strftime('%d %b %Y') # < Python 3.3
    return datetime.fromtimestamp(time_stamp, tz='UTC').strftime('%d %b %Y') # >= Python 3.3


def get_file_attrs_modif_time(folder: str) -> None:
    """
    Get file modification date and time

    :param folder: str folder to scan
    :return: None
    """
    with os.scandir(folder) as directory:
        for f in directory:
            if f.is_file():
                info = f.stat()
                print(f'Modified {get_date(info.st_mtime)} {f.name}')


def get_file_attrs_size(folder: str) -> None:
    """
    Get file size

    :param folder: str folder to scan
    :return: None
    """
    with os.scandir(folder) as directory:
        for f in directory:
            if f.is_file():
                info = f.stat()
                print(f'{f.name} {info.st_size} bytes')


def traverse_directory(folder: str) -> None:
    """
    Traverse a directory

    :param folder: str folder to traverse
    :return: None
    """
    with open('traverse_directory.txt', 'w', encoding='utf_8') as f:
        for folder_path, _, files in os.walk(folder):
            f.write(f'Folder: {folder_path}\n')
            # print(f'Folder: {folder_path}')
            for file_name in files:
                f.write(f'\t{file_name}\n')
                # print(f'\t{file_name}')


def copy_file(src: str, dst: str) -> None:
    """
    Alias function: Copy a file using shutil

    :param src: str source file
    :param dst: str destination file
    :return: None
    """
    shutil.copy(src, dst)


def copy_folder(src, dst):
    shutil.copytree(src, dst)


def move_file(src: str, dst: str) -> None:
    """
    Alias function: Move a file using shutil

    :param src: str source file
    :param dst: str destination file
    :return: None
    """
    shutil.move(src, dst)


def rename_file(src: str, dst: str) -> None:
    """
    Alias function: Rename a file

    :param src: str source file name
    :param dst: str destination file name
    :return: None
    """
    # os.rename(src, dst)
    f = Path(src)
    f.rename(dst)


def remove_file(f: object) -> None:
    """
    Alias function: Remove a file

    :param f: object file to remove
    :return: None
    """
    if not os.path.isfile(f):
        print(f'Error: {f} is not a valid file')
    else:
        try:
            os.remove(f)
        except OSError as e:
            print(f'Error: {f} : {e.strerror}')


if __name__ == '__main__':
    list_dir(Path(folder='.'))
    # traverse_directory(folder='.')
