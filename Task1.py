import requests
import time
from datetime import datetime, timedelta

def fetch_yandex_time():
    url = "https://yandex.com/time/sync.json?geo=213"

    # Засекаем локальное время до запроса 
    local_time_before = time.time()

    # Отправляем GET-запрос
    response = requests.get(url)

    # Засекаем локальное время после запроса (необходимо для того, чтобы понять, какое время проходит между первым временем (local_time_before) и временем, после которого совершился запрос)
    local_time_after = time.time()

    # Проверка, что ответ получен успешно
    if response.status_code != 200:
        print("Ошибка при выполнении запроса:", response.status_code)
        return None

    # Выводим JSON-ответ
    raw_data = response.json()
    print("Сырой ответ от сервера:", raw_data)

    # Извлекаем нужные данные
    server_time_ms = raw_data['time']      # Время на сервере в миллисекундах
    tz_name = raw_data.get('tzname', 'N/A') # Называние часового пояса 
    offset_sec = raw_data.get('offset', 0) # Смещение времени в соотвествии с часовым поясом 

    # Переводим миллисекунды в секунды и создаем datetime-объект
    server_time = datetime.utcfromtimestamp(server_time_ms / 1000.0) + timedelta(seconds=offset_sec)

    print("Человеко-понятное серверное время:", server_time.strftime('%Y-%m-%d %H:%M:%S'))
    print("Часовой пояс:", tz_name)

    # Среднее локальное время (приблизительно соответствует моменту получения ответа)
    local_time_avg = (local_time_before + local_time_after) / 2
    local_dt = datetime.utcfromtimestamp(local_time_avg)

    # Вычисляем дельту между локальным временем и временем с сервера
    delta = abs((server_time - local_dt).total_seconds())
    print(f"Дельта времени (сек): {delta:.3f}\n")

    return delta

# Повторяем 5 раз и считаем среднюю дельту
deltas = []
print("===== Серия из 5 запросов =====")
for i in range(5):
    print(f"--- Запрос {i+1} ---")
    delta = fetch_yandex_time()
    if delta is not None:
        deltas.append(delta)
    time.sleep(1)  # Задержка в 1 секунду между запросами 

# Расчет средней дельты
if deltas:
    avg_delta = sum(deltas) / len(deltas)
    print(f"Средняя дельта времени за 5 запросов: {avg_delta:.3f} сек")
else:
    print("Не удалось получить данные.")
