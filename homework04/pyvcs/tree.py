# type: ignore

import calendar
import datetime
import os
import pathlib
import stat
import time
import typing as tp
from pathlib import *

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    # вброс: Попробую на пальцах описать алгоритм:
    # def write-tree(индекс):
    #     tree_entries = []
    #     пройтись по каждой записи в индексе:
    #         если имеем дело с каталогом (lib/books/dune.txt):
    #             отсекаем первую часть пути (lib)
    #             формируем строку: "mode путь\x00sha" (путь это lib, второй раз, lib/books, попробуйте закоммитить несколько вложенных каталогов и посмотреть tree-obj)
    #             прибавляем к tree_entries
    #             вызываем write-tree для оставшегося пути (books/dune.txt)
    #         иначе, имеем дело с именем файла (dune.txt):
    #             формируем строку: "mode_в_8_й_системе имя_файла\x00sha"
    #             прибавляем к tree_entries
    #     данные = объединяем все tree_entries в длинную строку байт
    #     вернуть hash_object(данные, "tree", write=True)
    tree_entries = []
    index_quantity = len(index)
    for i in range(index_quantity):
        myname = index[i].name
        if len(dirname) > 0:
            myname = myname.replace(dirname + os.sep, "")
        sha = index[i].sha1
        mode = "{:6o}".format(index[i][6])  # output in octal number system
        if myname.find(os.sep) > -1:

            path_first_part = dirname + myname.split(os.sep)[0]
            path_second_part = myname.split(os.sep)[1:]
            my_tree_hash = bytes.fromhex(write_tree(gitdir, [index[i]], path_first_part))
            tree_entry = (
                ("40000").encode() + b" " + path_first_part.encode() + b"\x00" + my_tree_hash
            )
            tree_entries.append(tree_entry)

        else:
            tree_entry = mode.encode() + b" " + myname.encode() + b"\x00" + sha
            tree_entries.append(tree_entry)
    mydata = b""
    for j in tree_entries:
        mydata += j
    return hash_object(mydata, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    tree_hash = "tree " + tree
    if parent is None:
        parent_hash = ""
    else:
        parent_hash = parent
    if author is None:
        myauthor = ""
    else:
        myauthor = author

    n1 = time.localtime
    time_tuple = n1()[0:10]
    timestamp_ = time.mktime(time_tuple)
    now = datetime.datetime.today()
    tz1 = datetime.datetime.astimezone(now)
    tz1_str = str(tz1)[26:32].replace(":", "")
    timestamp_tz = str(timestamp_).split(".")[0] + " " + tz1_str
    data = (
        tree_hash
        + "\nauthor "
        + myauthor
        + " "
        + timestamp_tz
        + "\ncommitter "
        + myauthor
        + " "
        + timestamp_tz
        + "\n\n"
        + message
        + "\n"
    )
    return hash_object(data.encode(), "commit")
