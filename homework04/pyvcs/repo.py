import argparse
import os
import pathlib
import typing as tp
from pathlib import *


def parse():
    gd = ""

    # This is the code to use if git dir name is to be read from run parameters, not from the environment variable
    # parser = argparse.ArgumentParser()

    #
    # parser.add_argument(
    #     "--GIT_DIR",
    #     type=str,
    #     dest="gd",
    #     action="store",
    #     help="repo dir name",
    # )
    # args = parser.parse_args()
    #
    # if args.gd == '':
    #     gd = ".git"
    # else:
    #     gd = args.gd#os.environ["GIT_DIR"]

    # This is the code to use if git dir name is to be read from the environment variable

    gd = os.getenv("GIT_DIR", ".git")
    return gd


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    # tmp = os.walk(workdir) # I do this to print the whole tree for debug purpose
    # for i in tmp:
    #     print(i)
    if isinstance(
        workdir, str
    ):  # this is to convert workdir argument to type "Path" is it comes as "str"
        workdir1 = Path(workdir)
    else:
        workdir1 = workdir

    myname = parse()
    mypath = workdir1 / myname
    if mypath.exists():
        return mypath
    elif workdir1.parent.parent.exists() and (workdir1.parent.parent != Path(".")):
        return repo_find(workdir1.parent.parent)
    else:
        raise Exception("Not a git repository")
    pass


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    """ " creates a repo with correct structure according to the task,
    can create a git repo with any name, inside any given workdir,
    does not create a repo if the given workdir is a file"""
    if isinstance(
        workdir, str
    ):  # this is to convert workdir argument to type "Path" is it comes as "str"
        workdir1 = Path(workdir)
    else:
        workdir1 = workdir

    if Path.is_dir(workdir1):
        mypath = workdir1
    elif workdir == "":
        mypath = Path.cwd()
    else:
        raise Exception(f"{workdir1} is not a directory")

    GIT_DIR = parse()

    dir_name = GIT_DIR
    gitdir = mypath / dir_name
    gitdir.mkdir(parents=True, exist_ok=True)
    heads = mypath / dir_name / "refs" / "heads"
    heads.mkdir(parents=True, exist_ok=True)
    tags = mypath / dir_name / "refs" / "tags"
    tags.mkdir(parents=True, exist_ok=True)
    objects = mypath / dir_name / "objects"
    objects.mkdir(parents=True, exist_ok=True)

    os.chdir(gitdir)

    HEAD = open("HEAD", "a")
    HEAD.write("ref: refs/heads/master\n")
    HEAD.close()

    config = open("config", "a")
    config.write(
        "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n"
    )
    config.close()

    desc = open("description", "a")
    desc.write("Unnamed pyvcs repository.\n")
    desc.close()

    # tmp = os.walk('.') # I do this to print the whole tree for debug purpose
    # for i in tmp:
    #     print(i)

    os.chdir("..")  # I go back to make Rel.Path valid again otherwise the unittest won't work
    return gitdir
