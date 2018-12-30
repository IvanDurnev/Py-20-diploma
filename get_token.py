# функция для получения токена
from urllib.parse import urlencode, urlsplit

APP_ID = 6773685
AUTH_URL = 'https://oauth.vk.com/authorize?'
auth_params = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'scope': 'friends, email',
    'response_type': 'token',
    'v': '5.92'
}
print(AUTH_URL+urlencode(auth_params))