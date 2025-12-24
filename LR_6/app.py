from flask import Flask, render_template, jsonify, request  
from flask_socketio import SocketIO, emit, disconnect
from typing import Dict
import threading
import time
import logging
from datetime import datetime
from currency_tracker import CurrencyTracker
from websocket_observer import WebSocketObserver

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Замените на надежный ключ
socketio = SocketIO(app, cors_allowed_origins="*")

# Инициализация трекера
currency_tracker = CurrencyTracker(update_interval=30)
# Словарь для хранения связи между sid и наблюдателями
ws_observers: Dict[str, WebSocketObserver] = {}

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def background_update_task():
    """Фоновая задача для периодического обновления курсов валют"""
    logger.info("Фоновая задача обновления курсов запущена")
    
    while True:
        try:
            # Получаем данные с API
            if currency_tracker.fetch_currency_data():
                # Уведомляем всех наблюдателей об изменениях
                currency_tracker.notify_observers()
            
            # Ждем указанный интервал
            time.sleep(currency_tracker.update_interval)
            
        except Exception as e:
            logger.error(f"Ошибка в фоновой задаче: {e}")
            time.sleep(60)  # Ждем минуту при ошибке


@app.route('/')
def index():
    """Главная страница с клиентом WebSocket"""
    return render_template('index.html')


@app.route('/api/currencies')
def get_currencies():
    """API endpoint для получения текущих курсов валют"""
    currencies = currency_tracker.get_all_currencies()
    return jsonify({
        code: data.to_dict() for code, data in currencies.items()
    })


@app.route('/api/currencies/<code>')
def get_currency(code: str):
    """API endpoint для получения курса конкретной валюты"""
    currency = currency_tracker.get_currency(code)
    if currency:
        return jsonify(currency.to_dict())
    return jsonify({'error': 'Currency not found'}), 404


@socketio.on('connect')
def handle_connect():
    """Обработчик подключения нового WebSocket клиента"""
    sid = request.sid  # Получаем идентификатор сессии
    logger.info(f"Новое WebSocket подключение: {sid}")
    
    # Создаем наблюдателя для этого подключения
    observer = WebSocketObserver(socketio, sid)
    currency_tracker.register_observer(observer)
    ws_observers[sid] = observer
    
    # Отправляем приветственное сообщение с ID наблюдателя
    emit('connected', {
        'observer_id': observer.get_id(),
        'message': 'Connected to currency tracker',
        'timestamp': datetime.now().isoformat()
    })


@socketio.on('track_currency')
def handle_track_currency(data):
    """Обработчик запроса на отслеживание конкретных валют"""
    sid = request.sid
    observer = ws_observers.get(sid)
    
    if observer and 'currencies' in data:
        currencies = set(data['currencies'])
        observer.set_tracked_currencies(currencies)
        
        logger.info(f"Клиент {observer.get_id()} отслеживает валюты: {currencies}")
        emit('tracking_started', {
            'currencies': list(currencies),
            'message': f'Now tracking {len(currencies)} currencies'
        })


@socketio.on('disconnect')
def handle_disconnect():
    """Обработчик отключения WebSocket клиента"""
    sid = request.sid
    observer = ws_observers.pop(sid, None)
    
    if observer:
        currency_tracker.remove_observer(observer)
        logger.info(f"WebSocket отключен: {observer.get_id()}")


if __name__ == '__main__':
    # Запускаем фоновую задачу в отдельном потоке
    update_thread = threading.Thread(target=background_update_task, daemon=True)
    update_thread.start()
    
    # Запускаем Flask приложение с WebSocket поддержкой
    logger.info("Запуск сервера на http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)