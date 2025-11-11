from fastapi import FastAPI, Query
from typing import Optional ## с помощью Optional можно сделать часть значений необязательными
from pydantic import BaseModel ## для создания моделей данных, которые будут добавляться в словарь

app = FastAPI()

glossary = {
   1: {
      'term': 'Класс',
      'description': 'Шаблон для создания пользовательских объектов.'
   },
   2: {
      'term': 'Декоратор',
      'description': 'Функция, возвращающая другую функцию, обычно применяется для преобразования функций с помощью синтаксиса @wrapper.'
   },
   3: {
      'term': 'Словарь',
      'description': 'Ассоциативный массив, в котором произвольным ключам сопоставляются значения.'
   }
}

class TermInfo(BaseModel): ## чтобы API понимал, какие данные ждать от пользователя 
   term: str
   description: Optional[str] = None ## переменная description будет необязательной и по умолч. равной None

class UpdateTerm(BaseModel):
   term: Optional[str] = None
   description: Optional[str] = None

@app.get('/')
async def home():
   return {'Hello!': 'Welcome to the glossary!'}

@app.get('/get_all')
async def get_all():
   '''Получение всех терминов глоссария'''
   return glossary

@app.get('/get-term/{term_id}')
async def get_term(term_id: int):
   '''Получение термина по ID'''
   return glossary[term_id]

@app.get('/search-term')
async def search_term(keyword: str):
   '''Поиск термина по ключевому слову'''
   results = {}

   for term_id, term_data in glossary.items():
      if (keyword.lower() in term_data['term'].lower() or 
         keyword.lower() in term_data['description'].lower()):
         results[term_id] = term_data
    
   return results

@app.post('/create-term/{term_id}')
async def create_term(term_id: int, new_term: TermInfo):
   '''Создание термина'''
   if term_id in glossary:
      return {'Error': 'Term already exists'}
   
   glossary[term_id] = new_term
   return glossary[term_id]

@app.put('/update-term/{term_id}')
async def update_term(term_id: int, upd_term: UpdateTerm):
   '''Обновление термина'''
   if term_id not in glossary:
      return {'Error': 'Term ID does not exists'}
   if upd_term.term != None:
      glossary[term_id].term= upd_term.term
   if upd_term.description != None:
      glossary[term_id].description = upd_term.description
   return glossary[term_id]
   
@app.delete('/delete-term')
def delete_term(term_id: int = Query(..., description = 'The book ID must be greater than zero')):
   '''Удаление термина'''
   if term_id not in glossary:
      return {'Error': 'Term ID does not exists'}
   del glossary[term_id]
   return {'Done': 'The term successfully deleted'}