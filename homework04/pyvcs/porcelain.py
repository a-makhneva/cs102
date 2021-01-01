import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    # #
    # # вопрос: А индекс не должен удаляться после add? непонятно
    # #
    # # ответ: Без разницы, вам все равно нужно будет создать новый
    # Вызывает
    # update - index
    # с
    # аргументом
    # write = True.
    update_index(gitdir, paths, True)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    # Коммит читает индекс (read_index),
    # пишет дерево (write_tree)
    # так как в коммите должна быть ссылка на дерево,
    # определяет родителя (resolve_head),
    # так как у коммита может быть родитель ,
    # пишет сам коммит (commit_tree)
    # и обновляет (update_ref) содержимое HEAD,
    # если HEAD откреплен (detached),
    # иначе ветки куда указывает HEAD (get_ref)
    myindex = read_index(gitdir)
    mytree = write_tree(gitdir, myindex, "")
    myhead = resolve_head(gitdir)
    mycommit = commit_tree(gitdir, mytree, message, myhead, author)
    if is_detached(gitdir):
        update_ref(gitdir, resolve_head(gitdir), mycommit)
    else:
        update_ref(gitdir, resolve_head(gitdir), mycommit)
    pass


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    entries = read_index(gitdir)
    for entry in entries:
        path = entry.name
        os.remove(path)
    my_obj = find_object(obj_name, gitdir)


#     ...вопрос: какие файлы должны удаляться при чекауте и как их найти?
#
# ответ: Должны удаляться файлы, которые есть в индексе. Для чтения индекса у нас есть функция read_index,
# затем проходим по каждой записи, в записях есть пути к файлам и каталогам (name), которые и нужно удалить.
#
# вопрос: А по какой записи? Пытался удалять по tree из коммита, но коммиты пустые
#
# ответ: Грубо говоря:
# entries = read_index(gitdir)
# for entry in entries:
#     path = entry.name
#     remove(path)
#
# еще ответ: 1. Удалить файлы, на которые есть ссылки в индексе
# 2. Найти коммит на который делаем checkout
# 3. Извлечь из коммита ссылку на tree
# 4. Рекурсивно обойти tree и восстановить файлы:
# 1.Мы смотрим какие записи есть в индексе и их удаляем из рабочего каталога
# 2.Всамыхпервыхзаданияхприводитсяпример, какмыизобъектаможемвосстановитьегосодержимое, например, спомощьюкомандыcat - file.
# 3.Восстанавливаемфайлыврабочемкаталогевсоответствиискоммитом, накоторыйхотимпереключиться.\
#     Индексунасневалидный, таккаксодержитзаписиофайлах, которыемыудалили, надоегозановосоздать.
# 42 и43 могут не делать команду checkout.
# 5. Воссоздать индекс
# 6. Обновить ссылку, содержащуюся в HEAD
