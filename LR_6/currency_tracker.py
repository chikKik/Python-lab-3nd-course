import requests# работа с HTTP
from typing import Dict, List, Set, Optional
from xml.etree import ElementTree as ET# реализация API для парсинга и создания XML
from datetime import datetime, timedelta
import logging# регистрация событий
from interfaces import Subject, Observer, CurrencyData


class CurrencyTracker(Subject):
    """Класс для отслеживания курсов валют с API ЦБ РФ"""
    
    
    API_URL = "http://localhost:5001/scripts/XML_daily.asp"  
    
    def __init__(self, update_interval: int = 30):  
        """
        Инициализация трекера
        
        Args:
            update_interval: интервал обновления в секундах (по умолчанию 30)
        """
        self._observers: List[Observer] = []
        self._currencies: Dict[str, CurrencyData] = {}
        self._previous_currencies: Dict[str, CurrencyData] = {}
        self.update_interval = update_interval
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Используется API: {self.API_URL}")
    
    def register_observer(self, observer: Observer) -> None:
        """Регистрация нового наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)
            self.logger.info(f"Зарегистрирован наблюдатель: {observer.get_id()}")
    
    def remove_observer(self, observer: Observer) -> None:
        """Удаление наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)
            self.logger.info(f"Удален наблюдатель: {observer.get_id()}")
    
    def notify_observers(self) -> None:
        """Уведомление всех наблюдателей об изменениях"""
        if not self._observers:
            return
        
        changed_currencies = self._get_changed_currencies()
        
        if changed_currencies:
            self.logger.info(f"Обнаружены изменения в курсах: {list(changed_currencies.keys())}")
            for observer in self._observers:
                try:
                    observer.update(changed_currencies)
                except Exception as e:
                    self.logger.error(f"Ошибка уведомления наблюдателя {observer.get_id()}: {e}")
        else:
            self.logger.debug("Изменений в курсах не обнаружено")
    
    def _get_changed_currencies(self) -> Dict[str, CurrencyData]:
        """Получение валют, курс которых изменился"""
        changed = {}
        for code, current in self._currencies.items():
            previous = self._previous_currencies.get(code)
            
            # Если валюты не было в предыдущих данных или курс изменился
            if not previous or abs(current.value - previous.value) > 0.0001:
                changed[code] = current
        
        return changed
    
    def fetch_currency_data(self) -> bool:
        """
        Запрос данных с фейкового API ЦБ РФ
    
        Returns:
        bool: True если данные успешно получены, False в противном случае
        """
        try:
            # Добавляем параметр для избежания кэширования
            response = requests.get(self.API_URL, timeout=10, 
                            params={"_": datetime.now().timestamp()})
            response.raise_for_status()
        
            # Устанавливаем правильную кодировку для парсинга
            response.encoding = 'utf-8'
        
            # Парсинг XML
            root = ET.fromstring(response.content)
        
            # Сохраняем предыдущие данные перед обновлением
            self._previous_currencies = self._currencies.copy()
        
            # Очищаем текущие данные
            new_currencies = {}
        
            for valute in root.findall('Valute'):
                code = valute.find('CharCode').text
                name = valute.find('Name').text
                nominal = int(valute.find('Nominal').text)
                value_str = valute.find('Value').text.replace(',', '.')
                value = float(value_str)
            
                new_currencies[code] = CurrencyData(
                    code=code,
                    name=name,
                    value=value / nominal,  # Курс за 1 единицу
                    nominal=nominal,
                    last_updated=datetime.now()
                )
        
            # Только после успешного парсинга обновляем данные
            self._currencies = new_currencies
        
            self.logger.info(f"Получены данные для {len(self._currencies)} валют")
            return True
        
        except requests.RequestException as e:
            self.logger.error(f"Ошибка при запросе к API: {e}")
            self.logger.warning("Проверьте, запущен ли фейковый сервер на порту 5001")
            return False
        except ET.ParseError as e:
            self.logger.error(f"Ошибка парсинга XML: {e}")
            self.logger.error(f"Ответ сервера: {response.text[:500]}")
            return False
        except AttributeError as e:
            self.logger.error(f"Ошибка структуры XML: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка: {e}")
            return False

    
    def get_currency(self, code: str) -> Optional[CurrencyData]:
        """Получение данных по конкретной валюте"""
        return self._currencies.get(code.upper())
    
    def get_all_currencies(self) -> Dict[str, CurrencyData]:
        """Получение всех валют"""
        return self._currencies.copy()
    
    def get_tracked_codes(self) -> Set[str]:
        """Получение списка отслеживаемых кодов валют"""
        return set(self._currencies.keys())