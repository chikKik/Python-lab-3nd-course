from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional# явное указание типов данных
from dataclasses import dataclass
from datetime import datetime

@dataclass# поддерживает аннтоцию типов
class CurrencyData:
    """Класс для хранения данных о валюте"""
    code: str  # Код валюты (USD, EUR и т.д.)
    name: str  # Название валюты
    value: float  # Курс к рублю
    nominal: int  # Номинал
    last_updated: datetime  # Время последнего обновления
    
    def to_dict(self) -> Dict[str, Any]:# возвращает словарь со строковыми ключами
        """Преобразование в словарь для JSON"""
        return {
            'code': self.code,
            'name': self.name,
            'value': self.value,
            'nominal': self.nominal,
            'last_updated': self.last_updated.isoformat()
        }
    
class Observer(ABC):
    """Абстрактный класс Наблюдателя"""

    @abstractmethod
    def update(self, currency_data: Dict[str, CurrencyData]) -> None:
        """Метод для получения обновлений"""
        pass

    @abstractmethod
    def get_id(self) -> str:
        """Получение уникального идентификатора наблюдателя"""
        pass

class Subject(ABC):
    """Абстрактный класс Субъекта"""

    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        """Регистрация нового наблюдателя"""
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        """Удаление наблюдателя"""
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        """Уведомление всех наблюдателей"""
        pass




    




