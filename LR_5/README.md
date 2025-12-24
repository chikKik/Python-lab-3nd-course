# Python-lab-3nd-course
Создание виртуального окружения:
1. `python -m venv venv`
2. `.\venv\Scripts\activate`

Для генерации protobufs команда:
```bush
# Из корневой директории проекта
python -m grpc_tools.protoc -I./protobufs --python_out=. --pyi_out=. --grpc_python_out=. ./protobufs/glossary.proto
```
После выполнения команды появятся файлы:
- `glossary_pb2.py`
- `glossary_pb2.pyi`
- `glossary_pb2_grpc.py`

В первой консоли запустить: `python grpc_server.py`</br>
Во второй консоли запустить: `python web_api.py`