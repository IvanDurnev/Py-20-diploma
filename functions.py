from urllib.parse import urlsplit
from settings import TOKEN
from Vkapi import VkGroup


def find_secret_groups(user):
    groups = user.groups()['items']
    friends = user.friends()['items']
    print(f'У {user.first_name} {len(friends)} друзей и {len(groups)} групп')
    for group in groups:
        CurrentGroup = VkGroup(group, TOKEN)
        print(f'Проверяем группу {CurrentGroup.groupName}')
        for friend in friends:
            if CurrentGroup.is_member(friend):
                print(f'Друг {friend} тоже состоит в группе {group_name}, значит группа не подходит, берем следующую')
                groups.remove(group)
                break
            else:
                print(f'{friend} не в группе {group}')

    print(f'Группы в которых есть только {user.first_name} и нет его друзей:')
    for index, group in enumerate(groups):
        CurrentGroup = VkGroup(group, TOKEN)
        print(f"{index+1}) {CurrentGroup.groupName}")

def get_user_name(userLink):
    if 'http' in userLink:
        return urlsplit(userLink).path[1:]
    else:
        return userLink