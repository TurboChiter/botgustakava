import requests
import threading
import time

def update_github_file():
    # Параметры аутентификации GitHub
    username = 'TurboChiter'
    token = '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'

    # Параметры репозитория и файла
    repo_owner = 'TurboChiter'
    repo_name = 'botgustakava'
    file_path_in_repo = 'database.db'
    local_file_path = 'database.db'

    # URL для загрузки файла
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path_in_repo}'

    # Чтение содержимого файла
    with open(local_file_path, 'rb') as file:
        content = file.read()

    # Заголовки запроса с параметрами аутентификации
    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json',
    }

    # Параметры запроса
    params = {
        'message': 'Обновление файла',
        'content': content,
        'sha': None  # SHA хэш существующего файла, получите его с помощью API GitHub (GET /repos/:owner/:repo/contents/:path)
    }

    # Получение информации о файле для получения текущего SHA
    response = requests.get(url, headers=headers)
    response_json = response.json()
    params['sha'] = response_json['sha']

    # Обновление файла
    response = requests.put(url, headers=headers, json=params)

    # Печать результата
    if response.status_code == 200:
        print('Файл успешно обновлен.')
    else:
        print(f'Произошла ошибка: {response.status_code}, {response.text}')

    # Запланировать выполнение функции через 10 минут
    threading.Timer(600, update_github_file).start()

# Запустить обновление файла в первый раз
update_github_file()

# Оставить основной поток активным
threading.Event().wait()
