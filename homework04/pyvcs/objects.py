import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib
from pathlib import *
from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    content = data
    if fmt == 'blob':
        header = f"blob {len(content)}\0"
    elif fmt == 'tree':
        header = f"tree {len(content)}\0"
    elif fmt == 'commit':
        header = f"commit {len(content)}\0"
    byte_header = str.encode(header)
    store = byte_header + content
    result = hashlib.sha1(store).hexdigest()
    if write:
        mypath = repo_find(Path.cwd()) / "objects"
        os.chdir(str(mypath))
        header = mypath / result[0:2]
        header.mkdir(parents=True, exist_ok=True)
        os.chdir(str(header))
        body = result[2:]
        myfile = open(body, 'wb')
        myfile.write(zlib.compress(store))
        myfile.close()
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
    return result


def resolve_object(obj_name: object, gitdir: object) -> object:
    if not (4 <= len(obj_name) <= 40):  # length check
        raise Exception(f"Not a valid object name {obj_name}")
    result = []
    oldpath = Path.cwd().absolute()
    mypath = gitdir / "objects" / obj_name[0:2]  # git path /objects/ hash folder name
    myname = obj_name[2:]  # hash file name
    os.chdir(mypath.absolute())
    for root, dirs, files in os.walk(Path.cwd(), topdown=False):  # check all files in the folder git/objects/header
        for name in files:
            if name.startswith(myname):
                result.append(obj_name[0:2] + name)
    if result:  # result list is not empty? return it
        os.chdir(oldpath)
        return result
    os.chdir(oldpath)
    raise Exception(f"Not a valid object name {obj_name}")  # nothing found? => raise an exception


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    # PUT YOUR CODE HERE
    ...


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    MyObjects = resolve_object(sha, gitdir)
    oldpath = Path.cwd().absolute()
    result = tuple()
    for obj in MyObjects:
        header = gitdir / 'objects' / sha[0:2]
        os.chdir(str(header))
        body = sha[2:]
        myfile = open(body, 'rb')
        file_content = myfile.read()
        unpacked_content = zlib.decompress(file_content)
        unpacked_content_header = unpacked_content[0:8]
        unpacked_content_body = unpacked_content[8:]
        decoded_header = unpacked_content_header.decode().split()[0]  # split[0] is for the 1st word in the string
        # decoded_body = unpacked_content_body.decode()
        result += (decoded_header, unpacked_content_body)
        myfile.close()
    os.chdir(oldpath)
    return result


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    record_quantity = data.count(b' ')
    size = len(data)
    result = []
    data = data[1:]
    for i in range(0, record_quantity):
        mode = data.split(b' ')[0]
        first_word_length = len(mode) + 1
        data = data[first_word_length:]
        object_name = data.split(b'\x00')[0]
        second_word_length = len(object_name) + 1
        data = data[second_word_length:]

        third_word_length = 20
        sha = data[:third_word_length]
        data = data[third_word_length:]
        if i == record_quantity - 1:
            object_type = 'blob'
        else:
            object_type = 'tree'
        result.append(mode.decode() + ' ' + object_type + ' ' + sha.hex() + '\t' + object_name.decode())
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    oldpath = Path.cwd().absolute()
    gitdir = repo_find(Path.cwd())
    myobject = read_object(obj_name, gitdir)
    object_type = myobject[0]
    if object_type == 'tree':
        mytree = read_tree(myobject[1])
        for rec in mytree:
            first_word = rec.split()[0]
            if len(first_word) < 6:
                rec = '0' * (6 - len(first_word)) + rec
            print(rec)
    elif object_type == 'commit':
        mycommit = commit_parse(myobject[1])
        for rec in mycommit:
            print (rec)
    else:
        decoded_object = myobject[1].decode()
        print(decoded_object)
    os.chdir(oldpath)
    pass


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # PUT YOUR CODE HERE
    ...


def commit_parse(raw: bytes, start: int = 0, dct=None):
    result = []
    raw = raw [3:]  #cut off the leading symbols
    for _ in range(0, 5):
        first_word = raw.split(b'\n')[0]
        raw = raw.replace(first_word+b'\n', b'')
        result.append(first_word.decode())
    expected_output = "\n".join(
        [
            "tree 0c30406df9aea54b7fd6b48360417e59ab7ab9bb",
            "author Dementiy <Dementiy@yandex.ru> 1603404366 +0300",
            "committer Dementiy <Dementiy@yandex.ru> 1603404366 +0300",
            "",
            "initial commit",
        ]
    )
    return result
