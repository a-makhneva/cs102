import pathlib
import typing as tp
from pathlib import *
import os


def update_ref(gitdir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    oldpath = Path.cwd().absolute()
    mypath = gitdir
    os.chdir(mypath)
    myref = open(ref, "a")
    myref.write(new_value)
    myref.close()
    os.chdir(oldpath)


def symbolic_ref(gitdir: pathlib.Path, name: str, ref: str) -> None:
    with (gitdir / name).open(mode="w") as f:
        f.write("ref: " + ref)
    print(ref)


def ref_resolve(gitdir: pathlib.Path, refname: str) -> str:
    #     по    имени    или    пути    возвращает    содержимое.
    #     в    git    определен    такой    порядок    поиска
    #     https: // git - scm.com / docs / git - rev - parse:
    # 1.If $GIT_DIR / < refname > exists, that is what you mean(this is usually useful only for HEAD);
    # 2.otherwise, refs / < refname > if it exists;
    # 3. otherwise, refs / tags / < refname > if itexists;
    # 4. otherwise, refs / heads / < refname > if it exists;
    # 5.otherwise, refs / remotes / < refname > if it exists;
    # 6.otherwise, refs / remotes / < refname > / HEAD if it exists.

    if refname == 'HEAD':
        return resolve_head(gitdir)
    elif Path(gitdir / "refs" / refname).exists():
        mypath = gitdir / "refs" / refname
    elif Path(gitdir / "tags" / refname).exists():
        mypath = gitdir / "tags" / refname
    elif Path(gitdir / "heads" / refname).exists():
        mypath = gitdir / "heads" / refname
    elif Path(gitdir / "remotes" / refname).exists():
        mypath = gitdir / "remotes" / refname
    elif Path(gitdir / "remotes" / refname / "HEAD").exists():
        mypath = gitdir / "remotes" / refname / "HEAD"

    mypath = gitdir / refname
    myfile = open(mypath, "br")
    contents = myfile.read()
    myfile.close()
    return contents.decode()


def resolve_head(gitdir: pathlib.Path) -> tp.Optional[str]:
    mypath = gitdir / "HEAD"
    myfile = open(mypath, "br")
    contents = myfile.read()
    myfile.close()
    if contents.startswith(b'ref'):
        mypath = gitdir.absolute() / contents.strip().split()[1].decode()
    else:
        mypath = gitdir.absolute() / 'heads'  # here
    try:
        myfile = open(mypath, "br")
        contents = myfile.read()
        myfile.close()
    except:
        return None
    return contents.decode()


def is_detached(gitdir: pathlib.Path) -> bool:
    # определяет,    указывает     HEAD    на    ветку(например, refs / heads / master)
    # или    на    коммит, если    на    коммит, то    HEAD    в    detached    режиме.\
    #     Все    ссылки    на    ветки    начинаются    с    ref:

    mypath = gitdir / "HEAD"
    myfile = open(mypath, "br")
    contents = myfile.read()
    myfile.close()
    if contents.startswith(b'ref:'):
        return False
    else:
        return True


# Текущая ветка (положение в истории) определяется содержимым HEAD:
def get_ref(gitdir: pathlib.Path) -> str:
    oldpath = Path.cwd().absolute()
    mypath = gitdir
    os.chdir(mypath)
    HEAD = open("HEAD", 'r')
    file_content = HEAD.read()
    HEAD.close()
    os.chdir(oldpath)
    return file_content.strip().split()[1]
