# type: ignore

import hashlib
import operator
import os
import pathlib
import struct
import sys
import typing as tp
from pathlib import *
from stat import *

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        filename = self[12]
        null_bytes_quantity = (
            8 - (62 + len(filename)) % 8
        )  # How many null bytes to add to make size dividable by 8
        tail = b"\x00" * null_bytes_quantity
        filename_size = len(filename) + null_bytes_quantity
        values = (
            self[0],
            self[1],
            self[2],
            self[3],
            self[4],
            self[5],
            self[6],
            self[7],
            self[8],
            self[9],
            self[10],
            self[11],
            self[12].encode() + tail,
        )
        packed = struct.pack("!LLLLLLLLLL20sH" + str(filename_size) + "s", *values)
        return packed

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        myindex = data.index(b"\x00", 62)
        file_name_length = myindex - 62
        null_bytes_quantity = (
            8 - (62 + file_name_length) % 8
        )  # How many null bytes to add to make size dividable by 8
        struct_mask_tail = str(file_name_length + null_bytes_quantity) + "s"
        struct_mask = "!LLLLLLLLLL20sH" + struct_mask_tail
        result = struct.unpack(struct_mask, data)

        # The old pathetic way to calculate a struct mask with dynamic filename length
        # for i in range(4, 41):  # Let us take the filename length for granted
        #     struct_mask_tail = str(i) + "s"
        #     struct_mask = "!LLLLLLLLLL20sH" + struct_mask_tail
        #     try:
        #         result = struct.unpack(struct_mask, data)
        #         break
        #     except:
        #         continue  # The truth is out there

        expected_entry = GitIndexEntry(
            ctime_s=result[0],
            ctime_n=result[1],
            mtime_s=result[2],
            mtime_n=result[3],
            dev=result[4],
            ino=result[5],
            mode=result[6],
            uid=result[7],
            gid=result[8],
            size=result[9],
            sha1=result[10],
            flags=result[11],
            name=result[12].decode().rstrip("\x00"),
        )

        return expected_entry


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    olddir = Path.cwd().absolute()
    os.chdir(gitdir)
    try:
        index_file = open("index", "rb")
    except:
        return []  # If index doesnt exist
    byte_content = index_file.read()
    records_quantity_bytes = byte_content[8:12]
    records_quantity_number = struct.unpack("!L", records_quantity_bytes)[0]
    # records start at byte 12 and have size 62 + filename length
    current_record_begin = 12
    record_base_size = 62
    objs = [
        GitIndexEntry(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"\x00", 0, "")
        for i in range(records_quantity_number)
    ]  # init the result set
    for record_number in range(0, records_quantity_number):
        myindex = byte_content.index(b"\x00", current_record_begin + record_base_size)
        file_name_length = myindex - record_base_size - current_record_begin
        null_bytes_quantity = (
            8 - (record_base_size + file_name_length) % 8
        )  # How many null bytes to add to make size dividable by 8
        current_record_end = (
            current_record_begin + record_base_size + file_name_length + null_bytes_quantity
        )
        my_entry = GitIndexEntry(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"\x00", 0, "")
        data = byte_content[current_record_begin:current_record_end]
        unpacked_entry = my_entry.unpack(data)
        objs[record_number] = unpacked_entry
        current_record_begin = current_record_end
    index_file.close()
    os.chdir(olddir)
    return objs


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    olddir = Path.cwd().absolute()
    os.chdir(gitdir)
    index_file = open("index", "wb")
    entries_quantity = len(entries)
    byte_content = b"DIRC\x00\x00\x00\x02" + struct.pack("!L", entries_quantity)  # header
    for e in entries:
        byte_content += e.pack()
    digest = hashlib.sha1(byte_content).digest()
    index_file.write(byte_content + digest)
    index_file.close()
    os.chdir(olddir)


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    my_index = read_index(gitdir)
    for record in my_index:
        if details:
            mode = "{:6o}".format(record[6])  # output in octal number system
            stage = (record[11] >> 12) & 3
            print(mode, record[10].hex(), str(stage) + "\t" + record[12])
        else:
            print(record[12])


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    paths.sort()
    olddir = Path.cwd().absolute()
    files_quantity = len(paths)
    objs = [
        GitIndexEntry(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, b"\x00", 0, "") for i in range(files_quantity)
    ]  # init the result set
    for file_nr in range(files_quantity):
        myfilename = paths[file_nr]
        myfile = myfilename.open("br")
        myfile_contents = myfile.read()
        # myfile_contents_encoded = myfile_contents.encode()
        my_file_stat = os.stat(myfilename)
        st_file_attributes = my_file_stat.st_file_attributes

        my_entry = GitIndexEntry(
            my_file_stat[ST_CTIME],  # ctime
            0,  # ctime nano
            my_file_stat[ST_MTIME],  # mtime
            0,  # mtime nano
            my_file_stat[ST_DEV],  # dev
            my_file_stat[1],  # & 0xFFFFFFFF, #ino
            my_file_stat[ST_MODE],  # mode
            my_file_stat[ST_UID],  # uid
            my_file_stat[ST_GID],  # gid
            my_file_stat[ST_SIZE],  # size
            bytes.fromhex(hash_object(myfile_contents, "blob", True)),  # sha
            st_file_attributes,  # flags
            myfile.name,
        )  # name
        objs[file_nr] = my_entry
    write_index(gitdir, objs)
    os.chdir(olddir)
