from flask import Flask, render_template_string, request
import random
import threading
import time

app = Flask(__name__)

# Начальные фейковые курсы
rates = {
    "USD": 90.0,
    "EUR": 95.0,
    "GBP": 110.0,
    "CNY": 12.5,
    "JPY": 0.62
}

def auto_update_rates():
    """Автоматическое обновление курсов каждые 30 секунд"""
    while True:
        time.sleep(30)  # Обновляем каждые 30 секунд
        
        # Немного меняем курсы случайным образом
        for code in rates:
            change = random.uniform(-0.5, 0.5)  # Изменение от -0.5 до +0.5
            rates[code] = round(rates[code] + change, 2)
        
        print(f"[Фейковый ЦБ] Курсы обновлены: {rates}")
        
@app.route("/scripts/XML_daily.asp")
def fake_xml():
    """Эмуляция XML, как у ЦБ РФ с правильной кодировкой"""
    xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<ValCurs Date="07.11.2025" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>{{ usd }}</Value>
    </Valute>
    <Valute ID="R01239">
        <NumCode>978</NumCode>
        <CharCode>EUR</CharCode>
        <Nominal>1</Nominal>
        <Name>Евро</Name>
        <Value>{{ eur }}</Value>
    </Valute>
    <Valute ID="R01035">
        <NumCode>826</NumCode>
        <CharCode>GBP</CharCode>
        <Nominal>1</Nominal>
        <Name>Фунт стерлингов</Name>
        <Value>{{ gbp }}</Value>
    </Valute>
    <Valute ID="R01375">
        <NumCode>156</NumCode>
        <CharCode>CNY</CharCode>
        <Nominal>1</Nominal>
        <Name>Китайский юань</Name>
        <Value>{{ cny }}</Value>
    </Valute>
    <Valute ID="R01820">
        <NumCode>392</NumCode>
        <CharCode>JPY</CharCode>
        <Nominal>100</Nominal>
        <Name>Японская иена</Name>
        <Value>{{ jpy }}</Value>
    </Valute>
</ValCurs>
"""
    # форматируем в стиле ЦБ — запятая как разделитель
    def fmt(v): return f"{v:.4f}".replace('.', ',')
    
    response = render_template_string(xml_template,
        usd=fmt(rates["USD"]),
        eur=fmt(rates["EUR"]),
        gbp=fmt(rates["GBP"]),
        cny=fmt(rates["CNY"]),
        jpy=fmt(rates["JPY"])
    )
    
    # Устанавливаем правильный Content-Type для XML
    return response, 200, {'Content-Type': 'application/xml; charset=utf-8'}


@app.route("/fake_cbr", methods=["GET", "POST"])
def control_panel():
    """Панель управления для ручного изменения курсов"""
    global rates
    if request.method == "POST":
        for code in rates:
            val = request.form.get(code)
            if val:
                try:
                    rates[code] = float(val)
                except ValueError:
                    pass
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Фейковый ЦБ РФ - Панель управления</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; }
            .form-group { margin: 15px 0; }
            label { display: inline-block; width: 100px; }
            input { padding: 5px; width: 150px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .current-rates { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
            .links { margin-top: 20px; }
            .auto-update { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Фейковый ЦБ РФ</h1>
            
            <div class="current-rates">
                <h3>Текущие курсы:</h3>
                {% for code, value in rates.items() %}
                <p>{{ code }}: <strong>{{ "%.2f"|format(value) }} ₽</strong></p>
                {% endfor %}
                <p class="auto-update">⚠️ Автообновление каждые 30 секунд!</p>
            </div>
            
            <h3>Ручное изменение курсов:</h3>
            <form method="post">
                {% for code, value in rates.items() %}
                <div class="form-group">
                    <label>{{ code }}:</label>
                    <input type="number" name="{{ code }}" value="{{ "%.2f"|format(value) }}" step="0.01">
                </div>
                {% endfor %}
                <button type="submit">Сохранить изменения</button>
            </form>
            
            <div class="links">
                <h3>Ссылки:</h3>
                <ul>
                    <li><a href="/scripts/XML_daily.asp" target="_blank">Посмотреть XML (для трекера)</a></li>
                    <li><a href="http://localhost:5000" target="_blank">Перейти к трекеру валют</a></li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, rates=rates)

if __name__ == "__main__":
    # Запускаем автообновление в фоновом потоке
    update_thread = threading.Thread(target=auto_update_rates, daemon=True)
    update_thread.start()
    
    print("=" * 60)
    print("🚀 Фейковый сервис ЦБ РФ запущен!")
    print("📊 Доступные эндпоинты:")
    print("   • http://localhost:5001/fake_cbr - Панель управления")
    print("   • http://localhost:5001/scripts/XML_daily.asp - XML API")
    print("=" * 60)
    print("💡 Курсы автоматически меняются каждые 30 секунд")
    print("💡 Вы можете вручную менять курсы через панель управления")
    print("=" * 60)
    
    app.run(port=5001, debug=True)