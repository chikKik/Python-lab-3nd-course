from fastapi import FastAPI, Query, HTTPException
from typing import Optional, Dict, Any
import grpc
from pydantic import BaseModel

import glossary_pb2
import glossary_pb2_grpc

app = FastAPI()

# Pydantic модели
class TermBase(BaseModel):
    term: str
    description: Optional[str] = None

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    term: Optional[str] = None
    description: Optional[str] = None

class TermResponse(BaseModel):
    id: int
    term: str
    description: Optional[str] = None

# Модель для списка терминов
class TermItem(BaseModel):
    term: str
    description: Optional[str] = None

# Создаем gRPC канал
channel = grpc.insecure_channel('localhost:50051')
stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

@app.get('/')
async def home():
    try:
        response = stub.Home(glossary_pb2.Empty())
        return {'message': response.message}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get('/get_all')
async def get_all():
    '''Получение всех терминов глоссария'''
    try:
        response = stub.GetAll(glossary_pb2.Empty())
        
        # Преобразуем protobuf в словарь
        result = {}
        for term_id, term in response.terms.items():
            result[str(term_id)] = {  # Конвертируем ключ в строку
                'term': term.term,
                'description': term.description if term.description else None
            }
        return result
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get('/get-term/{term_id}', response_model=TermResponse)
async def get_term(term_id: int):
    '''Получение термина по ID'''
    try:
        response = stub.GetTerm(glossary_pb2.GetTermRequest(id=term_id))
        
        if response.error:
            raise HTTPException(status_code=404, detail=response.error)
        
        return {
            'id': response.id,
            'term': response.term,
            'description': response.description if response.description else None
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get('/search-term')
async def search_term(keyword: str = Query(..., min_length=1)):
    '''Поиск термина по ключевому слову'''
    try:
        response = stub.SearchTerm(glossary_pb2.SearchTermRequest(keyword=keyword))
        
        results = {}
        for term_id, term in response.results.items():
            results[str(term_id)] = {  # Конвертируем ключ в строку
                'term': term.term,
                'description': term.description if term.description else None
            }
        return results
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.post('/create-term/', response_model=TermResponse, status_code=201)
async def create_term(term_data: TermCreate):
    '''Создание термина'''
    try:
        request = glossary_pb2.CreateTermRequest(
            term=term_data.term,
            description=term_data.description if term_data.description else ""
        )
        
        response = stub.CreateTerm(request)
        
        return {
            'id': response.id,
            'term': response.term,
            'description': response.description if response.description else None
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.put('/update-term/{term_id}', response_model=TermResponse)
async def update_term(term_id: int, term_data: TermUpdate):
    '''Обновление термина'''
    try:
        request = glossary_pb2.UpdateTermRequest(id=term_id)
        
        if term_data.term is not None:
            request.term = term_data.term
        
        if term_data.description is not None:
            request.description = term_data.description
        
        response = stub.UpdateTerm(request)
        
        if response.error:
            raise HTTPException(status_code=404, detail=response.error)
        
        return {
            'id': response.id,
            'term': response.term,
            'description': response.description if response.description else None
        }
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.delete('/delete-term/{term_id}')
async def delete_term(term_id: int):
    '''Удаление термина'''
    try:
        response = stub.DeleteTerm(glossary_pb2.DeleteTermRequest(id=term_id))
        
        if response.error:
            raise HTTPException(status_code=404, detail=response.error)
        
        return {'Done': response.message}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)