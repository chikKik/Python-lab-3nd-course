#!/usr/bin/env python3
"""
Запуск двух сервисов одновременно:
1. Фейковый ЦБ РФ на порту 5001
2. Трекер валют на порту 5000
"""

import subprocess
import sys
import time
import webbrowser

def run_fake_cbr():
    """Запуск фейкового сервиса ЦБ РФ"""
    print("🚀 Запуск фейкового сервиса ЦБ РФ...")
    return subprocess.Popen([sys.executable, "fake_cbr.py"])

def run_currency_tracker():
    """Запуск трекера валют"""
    print("🚀 Запуск трекера валют...")
    return subprocess.Popen([sys.executable, "app.py"])

def main():
    print("=" * 60)
    print("🔄 Запуск двух сервисов:")
    print("   1. Фейковый ЦБ РФ (порт 5001)")
    print("   2. Трекер валют с WebSocket (порт 5000)")
    print("=" * 60)
    
    # Запускаем оба сервиса
    fake_cbr_process = run_fake_cbr()
    time.sleep(2)  # Даем первому сервису время запуститься
    
    tracker_process = run_currency_tracker()
    time.sleep(3)  # Даем второму сервису время запуститься
    
    print("\n" + "=" * 60)
    print("✅ Оба сервиса запущены!")
    print("\n🌐 Доступные страницы:")
    print("   • Панель управления фейкового ЦБ: http://localhost:5001/fake_cbr")
    print("   • Трекер валют: http://localhost:5000")
    print("\n📱 Открываю оба сервиса в браузере...")
    print("=" * 60)
    
    # Открываем в браузере
    webbrowser.open("http://localhost:5001/fake_cbr")
    webbrowser.open("http://localhost:5000")
    
    try:
        # Ждем завершения (по Ctrl+C)
        print("\n🛑 Нажмите Ctrl+C для остановки обоих сервисов")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Остановка сервисов...")
        fake_cbr_process.terminate()
        tracker_process.terminate()
        fake_cbr_process.wait()
        tracker_process.wait()
        print("✅ Сервисы остановлены")

if __name__ == "__main__":
    main()