from urllib.parse import urlsplit
from settings import TOKEN
from vkapi import VkGroup
import json


def save_result(username, groups):
    advanced_groups = {}
    for group in groups:
        CurrentGroup = VkGroup(group, TOKEN)
        advanced_groups.setdefault(group, []).append(CurrentGroup.groupName)
    json_advanced_groups = json.dumps(advanced_groups, ensure_ascii = False)
    with open(username+'.json', 'w') as result_file:
        result_file.write(json_advanced_groups)
    print(f'Результат проверки пользователя сохранен в файл "{username}.json"')

def find_secret_groups(user):
    groups = user.groups()['items']
    friends = user.friends()['items']
    print(f'У {user.first_name} {len(friends)} друзей и {len(groups)} групп')
    for group in groups:
        CurrentGroup = VkGroup(group, TOKEN)
        print(f'Проверяем группу {CurrentGroup.groupName}')
        for friend in friends:
            if CurrentGroup.is_member(friend):
                print(f'Друг {friend} тоже состоит в группе {CurrentGroup.groupName}, значит группа не подходит, берем следующую')
                groups.remove(group)
                break
            else:
                print(f'{friend} не в группе {group}')
    print(f'Группы в которых есть только {user.first_name} и нет его друзей:')
    for index, group in enumerate(groups):
        CurrentGroup = VkGroup(group, TOKEN)
        print(f"{index+1}) {CurrentGroup.groupName}")
    save_result(user.first_name+' '+user.last_name, groups)

def get_user_name(userLink):
    if 'http' in userLink:
        return urlsplit(userLink).path[1:]
    else:
        return userLink