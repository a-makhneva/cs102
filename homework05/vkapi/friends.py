# type: ignore

import dataclasses
import math
import time
import typing as tp

from vkapi import config, session
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    """
    Ответ на вызов метода `friends.get`.

    :param count: Количество пользователей.
    :param items: Список идентификаторов друзей пользователя или список пользователей.
    """

    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """

    params = {
        "user_id": user_id,
        "count": count,
        "offset": offset,
        "fields": fields,
        "access_token": config.VK_CONFIG["access_token"],
        "v": config.VK_CONFIG["version"],
    }

    response = session.get("friends.get", params).json()["response"]
    return FriendsResponse(count=response["count"], items=response["items"])


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """

    if target_uid:
        return session.get(
            "friends.getMutual",
            params={
                "source_uid": source_uid,
                "target_uid": target_uid,
                "order": order,
                "count": count,
                "offset": offset,
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
            },
        ).json()["response"]

    friends_list = range(0, len(target_uids), 100)
    if progress is not None:
        friends_list = progress(friends_list)

    final_list: tp.List[MutualFriends] = []

    for i in friends_list:
        response = session.get(
            "friends.getMutual",
            params={
                "source_uid": source_uid,
                "target_uids": ",".join([str(j) for j in target_uids[i : i + 100]]),
                "order": order,
                "count": count,
                "offset": offset + i,
                "access_token": config.VK_CONFIG["access_token"],
                "v": config.VK_CONFIG["version"],
            },
        ).json()["response"]

        final_list.extend(
            MutualFriends(
                id=num["id"], common_friends=num["common_friends"], common_count=num["common_count"]
            )
            for num in response
        )
        time.sleep(0.30)
    return final_list
