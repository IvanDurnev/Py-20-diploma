import requests
from settings import REQUEST_URL
from time import sleep


class VkAPI:
    token = ''

    def _request_get(self, method, request_parameters):
        number_of_attempts = 10
        for i in range(number_of_attempts):
            try:
                response = requests.get(REQUEST_URL + method, request_parameters).json()
                return response['response']
            except KeyError:
                print(f"Не удалось получить ответ от сервера, попыток {i}")
                if 'error' in response.keys():
                    print(f"{response['error']['error_msg']}")
                sleep(1)
                return None

class VkUser(VkAPI):
    id_num = ''
    id_txt = ''
    first_name = ''
    last_name = ''
    nickname = ''
    invalidUser = False

    def __init__(self, id_num, token):
        self.id_num = id_num
        self.token = token
        self._check_user(self.info())

    def _check_user(self, information):
        if information != None:
            if 'deactivated' not in information[0]:
                self.first_name = information[0]['first_name']
                self.last_name = information[0]['last_name']
                if self.id_num != information[0]['id']:
                    self.id_txt = self.id_num
                    self.id_num = information[0]['id']
                print(f'С нами {self.id_num} {self.first_name} {self.last_name}')
            else:
                print('Пользователь удален или заблокирован')
                self.invalidUser = True
            if 'is_closed' in information[0] and information[0]['is_closed'] == True:
                print('Это приватный аккаунт')
                self.invalidUser = True
        else:
            print('Уточните вводимые данные и попробуйте еще раз')
            self.invalidUser = True

    def info(self):
        method = 'users.get'
        request_parameters = {
            'user_ids': self.id_num,
            'access_token': self.token,
            'v': '5.92'
        }
        return self._request_get(method, request_parameters)

    def groups(self):
        method = 'groups.get'
        request_parameters = {
            'user_id': self.id_num,
            'access_token': self.token,
            'v': '5.92'
        }
        return self._request_get(method, request_parameters)

    def friends(self, count=None):
        method = 'friends.get'
        request_parameters = {
            'user_id': self.id_num,
            'access_token': self.token,
            'count': count,
            'v': '5.92'
        }
        return self._request_get(method, request_parameters)

    def group_members(self, group_id):
        method = 'groups.getMembers'
        request_parameters = {
            'group_id': group_id,
            'filter': 'friends',
            'access_token': self.token,
            'v': '5.92'
        }
        return self._request_get(method, request_parameters).json()['response']

class VkGroup(VkAPI):
    groupName = ''
    groupId = ''

    def __init__(self, groupId, token):
        self.groupId = groupId
        self.token = token
        information = self.group_info()
        self.groupName = information[0]['name']

    def group_info(self):
        method = 'groups.getById'
        request_parameters = {
            'group_id': self.groupId,
            'filter': 'friends',
            'access_token': self.token,
            'v': '5.92'
        }
        return self._request_get(method, request_parameters)

    def is_member(self, user_id):
        method = 'groups.isMember'
        request_parameters = {
            'group_id': self.groupId,
            'user_id': user_id,
            'filter': 'friends',
            'access_token': self.token,
            'v': '5.92'
        }
        return self._request_get(method, request_parameters)