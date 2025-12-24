from fastapi import FastAPI, Query
from typing import Optional
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Создаем подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('glossary.db')
    conn.row_factory = sqlite3.Row  # Чтобы получать результаты как словарь
    return conn

# Создаем таблицу при запуске
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS glossary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            term TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Вызываем создание таблицы при старте приложения
create_table()

class TermInfo(BaseModel):
    term: str
    description: Optional[str] = None

class UpdateTerm(BaseModel):
    term: Optional[str] = None
    description: Optional[str] = None

@app.get('/')
async def home():
    return {'Hello!': 'Welcome to the glossary!'}

@app.get('/get_all')
async def get_all():
    '''Получение всех терминов глоссария'''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM glossary')
    terms = cursor.fetchall()
    conn.close()
    
    # Преобразуем результаты в словарь
    result = {}
    for term in terms:
        result[term['id']] = {
            'term': term['term'],
            'description': term['description']
        }
    return result

@app.get('/get-term/{term_id}')
async def get_term(term_id: int):
    '''Получение термина по ID'''
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM glossary WHERE id = ?', (term_id,))
    term = cursor.fetchone()
    conn.close()
    
    if term is None:
        return {'Error': 'Term not found'}
    
    return {
        'id': term['id'],
        'term': term['term'],
        'description': term['description']
    }

@app.get('/search-term')
async def search_term(keyword: str):
    '''Поиск термина по ключевому слову'''
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ищем в названии термина и описании
    cursor.execute('''
        SELECT * FROM glossary 
        WHERE LOWER(term) LIKE ? OR LOWER(description) LIKE ?
    ''', (f'%{keyword.lower()}%', f'%{keyword.lower()}%'))
    
    terms = cursor.fetchall()
    conn.close()
    
    results = {}
    for term in terms:
        results[term['id']] = {
            'term': term['term'],
            'description': term['description']
        }
    return results

@app.post('/create-term/')
async def create_term(new_term: TermInfo):
    '''Создание термина'''
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO glossary (term, description)
        VALUES (?, ?)
    ''', (new_term.term, new_term.description))
    
    conn.commit()
    term_id = cursor.lastrowid
    conn.close()
    
    return {
        'id': term_id,
        'term': new_term.term,
        'description': new_term.description
    }

@app.put('/update-term/{term_id}')
async def update_term(term_id: int, upd_term: UpdateTerm):
    '''Обновление термина'''
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Сначала проверяем, существует ли термин
    cursor.execute('SELECT * FROM glossary WHERE id = ?', (term_id,))
    term = cursor.fetchone()
    
    if term is None:
        conn.close()
        return {'Error': 'Term ID does not exists'}
    
    # Обновляем только те поля, которые переданы
    updates = []
    values = []
    
    if upd_term.term is not None:
        updates.append("term = ?")
        values.append(upd_term.term)
    
    if upd_term.description is not None:
        updates.append("description = ?")
        values.append(upd_term.description)
    
    if updates:
        values.append(term_id)
        sql = f"UPDATE glossary SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, values)
        conn.commit()
    
    # Получаем обновленный термин
    cursor.execute('SELECT * FROM glossary WHERE id = ?', (term_id,))
    updated_term = cursor.fetchone()
    conn.close()
    
    return {
        'id': updated_term['id'],
        'term': updated_term['term'],
        'description': updated_term['description']
    }

@app.delete('/delete-term/{term_id}')
async def delete_term(term_id: int):
    '''Удаление термина'''
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Сначала проверяем, существует ли термин
    cursor.execute('SELECT * FROM glossary WHERE id = ?', (term_id,))
    term = cursor.fetchone()
    
    if term is None:
        conn.close()
        return {'Error': 'Term ID does not exists'}
    
    cursor.execute('DELETE FROM glossary WHERE id = ?', (term_id,))
    conn.commit()
    conn.close()
    
    return {'Done': 'The term successfully deleted'}
