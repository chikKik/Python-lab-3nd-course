import json
from typing import Dict
from flask_socketio import SocketIO, emit
import uuid # уникальные идентификаторы
from interfaces import Observer, CurrencyData
from datetime import datetime

class WebSocketObserver(Observer):
    """Наблюдатель, отправляющий обновления через WebSocket"""
    
    def __init__(self, socketio: SocketIO, sid: str):
        """
        Инициализация WebSocket наблюдателя
        
        Args:
            socketio: экземпляр SocketIO
            sid: идентификатор WebSocket сессии
        """
        self.socketio = socketio
        self.sid = sid
        self.observer_id = f"ws_{uuid.uuid4().hex[:8]}"
        self.tracked_currencies: set = set()  # Валюты, которые отслеживает этот клиент
    
    def update(self, currency_data: Dict[str, CurrencyData]) -> None:
        """
        Отправка обновлений клиенту через WebSocket
        
        Args:
            currency_data: словарь с измененными данными о валютах
        """
        # Фильтруем только те валюты, которые отслеживает клиент
        if self.tracked_currencies:
            filtered_data = {
                code: data for code, data in currency_data.items() 
                if code in self.tracked_currencies
            }
        else:
            filtered_data = currency_data  # Отправляем все, если нет фильтра
        
        if filtered_data:
            # Преобразуем данные в словарь для JSON
            data_to_send = {
                code: data.to_dict() for code, data in filtered_data.items()
            }
            
            try:
                self.socketio.emit(
                    'currency_update',
                    {
                        'observer_id': self.observer_id,
                        'currencies': data_to_send,
                        'timestamp': datetime.now().isoformat()
                    },
                    room=self.sid
                )
            except Exception as e:
                print(f"Ошибка отправки WebSocket для {self.observer_id}: {e}")
    
    def get_id(self) -> str:
        """Получение уникального идентификатора наблюдателя"""
        return self.observer_id
    
    def set_tracked_currencies(self, currencies: set) -> None:
        """Установка списка отслеживаемых валют"""
        self.tracked_currencies = currencies
    
    def add_tracked_currency(self, currency_code: str) -> None:
        """Добавление валюты для отслеживания"""
        self.tracked_currencies.add(currency_code.upper())
    
    def remove_tracked_currency(self, currency_code: str) -> None:
        """Удаление валюты из отслеживаемых"""
        self.tracked_currencies.discard(currency_code.upper())