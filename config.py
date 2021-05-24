import os

# Конфигурационный файл. Сюда лучше выносить названия, пути к файлам и прочие настраиваемые параметры
CFG = {
    'aggregators': {
        'shikimori': {
            'name': 'Shikimori',
            'site': 'https://shikimori.one',

            'auth': {
                'client_id': '',
                'client_secret': '',
                'authorization_code': '',
                'shiki_token_file': 'resources/ShikiToken.json'
            }
        }
    }
}

# главная директория
MAIN_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\'
