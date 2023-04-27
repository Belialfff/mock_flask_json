from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# исходная информация о пользователе


# генерация UUID
def generate_uuid():
    return uuid.uuid1()

# генерация даты в нужном формате
def time_now():
    current_time = datetime.now().isoformat(sep="T", timespec="seconds")
    return current_time

@app.route('/json/', methods=['POST'])
def update_user_info():
    # добавление параметра action
    action = request.args.get('action')
    # проверка параметра
    if action == 'add':
        # Получаем JSON-тело из запроса
        request_data = request.get_json()
        tickers = request_data['info']['tickers']
        # Извлекаем параметры из JSON-тела
        name = request_data['add']['name']
        timeFrame = request_data['add']['timeFrame']
        percent = request_data['add']['percent']

        # Добавляем новый тикер в список
        new_ticker = {
            "ticker": name,
            "alerts": [
                {
                    "timeframe": timeFrame,
                    "percent": percent
                }
            ]
        }
        tickers.append(new_ticker)

        # Формируем и возвращаем JSON-ответ
        response_data = {
            "info": {
                "userID": request_data['info']['userID'],
                "tickers": tickers
            },
            "uuid": generate_uuid(),
            "lastUpdate": time_now()
        }
        return jsonify(response_data)

    elif action == 'delete':
        request_data = request.get_json()

        # Извлекаем параметры из JSON-тела
        tickerName = request_data['delete']['name']
        alertIndex = request_data['delete']['alertIndex']
        tickers = request_data['info']['tickers']

        # Получаем список тикеров из JSON-тела
        tickers = request_data['info']['tickers']

        # Ищем нужный тикер в списке
        ticker_found = False
        for ticker in tickers:
            if ticker['ticker'] == tickerName:
                ticker_found = True
                # Проверяем наличие индекса в списке оповещений для данного тикера
                if alertIndex < len(ticker['alerts']):
                    # Удаляем запись об оповещении по индексу
                    ticker['alerts'].pop(alertIndex)
                else:
                    return jsonify({"error": "Index out of range"})
                break

        if not ticker_found:
            return jsonify({"error": "Ticker not found"})

        # Формируем и возвращаем JSON-ответ
        response_data = {
            "info": {
                "userID": request_data['info']['userID'],
                "tickers": tickers
            },
            "uuid": generate_uuid(),
            "lastUpdate": time_now()
        }
        return jsonify(response_data)

    # в случае передачи неверного значения action в ответ приходит сообщение об ошибке
    else:
        return jsonify({
            'error': 'Передан некорректный action - {}'.format(action)
        })

# запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8090, debug=True)
