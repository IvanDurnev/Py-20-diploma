import requests
import sys
from urllib.parse import urlsplit

TOKEN = 'd1ce10ef0d87f5de82498e4ed7bb1c79a0dee7cdb0dc4578fca9eb657960b4460c87158e3120c54b97137'

class VK_user:
    id = ''
    id_txt = ''
    first_name = ''
    last_name = ''
    nickname = ''

    reqest_url = 'https://api.vk.com/method/'

    def __init__(self, id):
        self.id = id
        information = self.info()
        self.first_name = information['first_name']
        self.last_name = information['last_name']
        if self.id != information['id']:
            self.id_txt = self.id
            self.id = information['id']
        print(f'С нами {self.id} {self.first_name} {self.last_name}')

    def info(self):
        method = 'users.get'
        request_parameters = {
            'user_ids': self.id,
            'access_token': TOKEN,
            'v': '5.92'
        }
        response = requests.get(self.reqest_url + method, request_parameters)
        return response.json()['response'][0]

    def groups(self):
        method = 'groups.get'
        request_parameters = {
            'user_id': self.id,
            'access_token': TOKEN,
            'v': '5.92'
        }
        response = requests.get(self.reqest_url+method, request_parameters)
        return response.json()['response']

    def friends(self):
        method = 'friends.get'
        request_parameters = {
            'user_id': self.id,
            'access_token': TOKEN,
            'count': 10, # ограничил для ускорения
            'v': '5.92'
        }
        response = requests.get(self.reqest_url + method, request_parameters)
        return response.json()['response']

    def group_members(self, group_id):
        method = 'groups.getMembers'
        request_parameters = {
            'group_id': group_id,
            'filter': 'friends',
            'access_token': TOKEN,
            'v': '5.92'
        }
        response = requests.get(self.reqest_url + method, request_parameters)
        return response.json()['response']


def group_info(group_id):
    reqest_url = 'https://api.vk.com/method/'
    method = 'groups.getById'
    request_parameters = {
        'group_id': group_id,
        'filter': 'friends',
        'access_token': TOKEN,
        'v': '5.92'
    }
    response = requests.get(reqest_url + method, request_parameters)
    return response.json()['response']

def is_member(user_id, group_id):
    reqest_url = 'https://api.vk.com/method/'
    method = 'groups.isMember'
    request_parameters = {
        'group_id': group_id,
        'user_id': user_id,
        'filter': 'friends',
        'access_token': TOKEN,
        'v': '5.92'
    }
    response = requests.get(reqest_url + method, request_parameters)
    return response.json()['response']

def find_secret_groups(user):
    groups = user.groups()['items']
    friends = user.friends()['items']
    print(groups)
    print(f'У {user.first_name} {len(friends)} друзей и {len(groups)} групп')
    for group in groups:
        group_name = group_info(group)[0]['name']
        print(f'Проверяем группу {group_name}')
        for friend in friends:
            if is_member(friend, group):
                print(f'Друг {friend} тоже состоит в группе {group_name}, значит группа не подходит, берем следующую')
                groups.remove(group)
                break
            else:
                print(f'{friend} не в группе {group}')

    print(f'Группы в которых есть только {user.first_name} и нет его друзей:')
    for index, group in enumerate(groups):
        print(f"{index+1}) {group_info(group)[0]['name']}")

def get_user_name(user_link):
    if 'http' in user_link:
        return urlsplit(user_link).path[1:]
    else:
        return user_link


if __name__ == '__main__':
    if len(sys.argv)>1:
        user_link = sys.argv[1]
    else:
        user_link = input('Какого пользователя проверим (ссылка на страницу, id)?\n')
    user = get_user_name(user_link)
    ivan = VK_user(user)
    find_secret_groups(ivan)