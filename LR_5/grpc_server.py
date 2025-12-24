import grpc
from concurrent import futures
import sqlite3

import glossary_pb2
import glossary_pb2_grpc

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self):
        # Создаем подключение к базе данных
        self.conn = sqlite3.connect('glossary.db', check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_table()
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS glossary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()
    
    def Home(self, request, context):
        return glossary_pb2.HomeResponse(message="Hello! Welcome to the glossary gRPC service!")
    
    def GetAll(self, request, context):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM glossary')
        terms = cursor.fetchall()
        
        response = glossary_pb2.GetAllResponse()
        
        for term in terms:
            term_msg = glossary_pb2.Term(
                id=term['id'],
                term=term['term'],
                description=term['description'] if term['description'] else ""
            )
            response.terms[term['id']].CopyFrom(term_msg)
        
        return response
    
    def GetTerm(self, request, context):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM glossary WHERE id = ?', (request.id,))
        term = cursor.fetchone()
        
        if term is None:
            return glossary_pb2.TermResponse(error="Term not found")
        
        return glossary_pb2.TermResponse(
            id=term['id'],
            term=term['term'],
            description=term['description'] if term['description'] else ""
        )
    
    def SearchTerm(self, request, context):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT * FROM glossary 
            WHERE LOWER(term) LIKE ? OR LOWER(description) LIKE ?
        ''', (f'%{request.keyword.lower()}%', f'%{request.keyword.lower()}%'))
        
        terms = cursor.fetchall()
        
        response = glossary_pb2.SearchTermResponse()
        
        for term in terms:
            term_msg = glossary_pb2.Term(
                id=term['id'],
                term=term['term'],
                description=term['description'] if term['description'] else ""
            )
            response.results[term['id']].CopyFrom(term_msg)
        
        return response
    
    def CreateTerm(self, request, context):
        cursor = self.conn.cursor()
        
        cursor.execute('''
            INSERT INTO glossary (term, description)
            VALUES (?, ?)
        ''', (request.term, request.description if request.description else None))
        
        self.conn.commit()
        term_id = cursor.lastrowid
        
        return glossary_pb2.TermResponse(
            id=term_id,
            term=request.term,
            description=request.description if request.description else ""
        )
    
    def UpdateTerm(self, request, context):
        cursor = self.conn.cursor()
        
        # Проверяем существование термина
        cursor.execute('SELECT * FROM glossary WHERE id = ?', (request.id,))
        term = cursor.fetchone()
        
        if term is None:
            return glossary_pb2.TermResponse(error="Term ID does not exist")
        
        # Подготавливаем запрос на обновление
        updates = []
        values = []
        
        if request.term:
            updates.append("term = ?")
            values.append(request.term)
        
        if request.HasField("description"):
            updates.append("description = ?")
            values.append(request.description)
        
        if updates:
            values.append(request.id)
            sql = f"UPDATE glossary SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(sql, values)
            self.conn.commit()
        
        # Получаем обновленный термин
        cursor.execute('SELECT * FROM glossary WHERE id = ?', (request.id,))
        updated_term = cursor.fetchone()
        
        return glossary_pb2.TermResponse(
            id=updated_term['id'],
            term=updated_term['term'],
            description=updated_term['description'] if updated_term['description'] else ""
        )
    
    def DeleteTerm(self, request, context):
        cursor = self.conn.cursor()
        
        # Проверяем существование термина
        cursor.execute('SELECT * FROM glossary WHERE id = ?', (request.id,))
        term = cursor.fetchone()
        
        if term is None:
            return glossary_pb2.DeleteResponse(error="Term ID does not exist")
        
        cursor.execute('DELETE FROM glossary WHERE id = ?', (request.id,))
        self.conn.commit()
        
        return glossary_pb2.DeleteResponse(message="The term successfully deleted")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()