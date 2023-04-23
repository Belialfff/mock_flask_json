from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# исходная информация о пользователе
USER_INFO = {
    "userID": "LT2567026",
    "tickers": [
        {
            "ticker": "M",
            "alerts": [
                {
                    "timeframe": 5,
                    "percent": 1
                },
                {
                    "timeframe": 10,
                    "percent": 5
                }
            ]
        },
        {
            "ticker": "A",
            "alerts": [
                {
                    "timeframe": 60,
                    "percent": 10
                },
                {
                    "timeframe": 10,
                    "percent": 5
                }
            ]
        }
    ]
}

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
        # ожидаемые в теле json параметры, прим.:
        """
        {
    "tickerName" : "str",
    "timeframe" : int,
    "percent" : int
           }
        """
        data = request.json
        tickerName = data.get('tickerName')
        timeframe = data.get('timeframe')
        percent = data.get('percent')
        ticker_info = None
        # проверка, есть ли в теле тикер с таким же именем
        for ticker in USER_INFO['tickers']:
            if ticker['ticker'] == tickerName:
                ticker_info = ticker
                break
        # если тикера нет - создаём его и добавляем в него "alert"
        if ticker_info is None:
            ticker_info = {
                'ticker': tickerName,
                'alerts': []
            }
            USER_INFO['tickers'].append(ticker_info)
        alerts = ticker_info['alerts']
        alerts.append({'timeframe': timeframe, 'percent': percent})

        # возвращаем изменённый "USER_INFO" с параметрами 'uuid' и 'lastUpdate'
        return jsonify({
            'uuid': generate_uuid(),
            'lastUpdate': time_now(),
            'info': USER_INFO
        })
    elif action == 'delete':
        # ожидаемые в теле json параметры вида:
        """
        {
    "tickerName" : "str",
    "alertIndex" : int
           }
        """
        data = request.json
        tickerName = data.get('tickerName')
        alertIndex = data.get('alertIndex')

        # проход по "tiker" в теле "USER_INFO"
        for ticker in USER_INFO['tickers']:
            if ticker['ticker'] == tickerName:
                alerts = ticker['alerts']
                # проверяем, существует ли alert по заданному индексу
                if alertIndex < len(alerts):
                    # удаляем alert по индексу
                    del alerts[alertIndex]
                    # возвращаем изменённый "USER_INFO" с параметрами 'uuid' и 'lastUpdate'
                    return jsonify({
                        'uuid': generate_uuid(),
                        'lastUpdate': time_now(),
                        'info': USER_INFO,
                    })
                else:
                    # в случае, если alert не найден
                    return jsonify({
                        'error': 'Alert not found'
                    })
        # на случай, если тикер не найден
        return jsonify({
            'error': 'Ticker not found'
        })

    # в случае передачи неверного значения action в ответ приходит сообщение об ошибке
    else:
        return jsonify({
            'error': 'Invalid action - {}'.format(action)
        })

# запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
