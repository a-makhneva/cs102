import os
import pathlib
import typing as tp
from pathlib import *
import argparse


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    return workdir / ".git"

def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    """" creates a repo with correct structure according to the task,
    can create a git repo with any name, inside any given workdir,
    does not create a repo if the given workdir is a file """
    temptype=type(workdir)
    if Path.is_dir(workdir):
        mypath = workdir
    elif workdir == '':
        mypath = Path.cwd()
    else:
        raise Exception(f"{workdir} is not a directory")

    """to do: should be able to name the repo"""

    # def parse():
    #     GIT_DIR = '0'
    #     parser.add_argument(
    #         "GIT-DIR",
    #         dest="GIT_DIR",
    #         action="store",
    #         help="stores given name of git repo",
    #     )
    #     return GIT_DIR

    def parse():
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "GIT-DIR",
            dest="GIT_DIR",
            action="store",
            help="stores given name of git repo",
        )
        GIT_DIR = parser.parse_args()

        if GIT_DIR == '':
            GIT_DIR = ".git"
        else:
            GIT_DIR = "{GIT_DIR}"
        return GIT_DIR

    # GIT_DIR = parse()
    # if GIT_DIR == '':
    #     GIT_DIR = ".git"
    # else:
    #     GIT_DIR = "{GIT_DIR}"

    # Path.mkdir(Path(str(mypath)+"/.git"))
    # os.chdir(Path(str(mypath)+"/.git"))
    # Path.mkdir("refs/heads")
    # Path.mkdir("refs/tags")
    # Path.mkdir("objects")
    dir_name = os.environ["GIT_DIR"]
    # mypath = pathlib.Path(workdir)
    gitdir = mypath / dir_name
    gitdir.mkdir(parents=True)
    heads = mypath / dir_name / "refs" / "heads"
    heads.mkdir(parents=True)
    tags = mypath / dir_name / "refs" / "tags"
    tags.mkdir(parents=True)
    objects = mypath / dir_name / "objects"
    objects.mkdir(parents=True)
    os.chdir(gitdir)


    HEAD = open("HEAD.txt", "a")
    HEAD.write("ref: refs/heads/master\n")
    HEAD.close()

    config = open("config.txt", "a")
    config.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")
    config.close()

    desc = open("description.txt", "a")
    desc.write("Unnamed pyvcs repository")
    desc.close()

    # print(1)
    # print(str(path)+"\.git")
    # qq =  pathlib.Path(str(path)+"\.git")
    # return qq
    return gitdir
