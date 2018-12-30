import sys
from Vkapi import VkUser
from functions import get_user_name, TOKEN, find_secret_groups


if __name__ == '__main__':
    if len(sys.argv)>1:
        userLink = sys.argv[1]
    else:
        userLink = input('Какого пользователя проверим (ссылка на страницу, id)?\n')
    userName = get_user_name(userLink)
    user = VkUser(userName, TOKEN)
    if not user.invalidUser:
        try:
            find_secret_groups(user)
        except KeyboardInterrupt:
            print('Программа прервана пользователем')