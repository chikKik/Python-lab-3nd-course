# # А теперь опишем функцию, в которой мы 
# # для "перехваченного" адреса URL модуля будем делать импорт

# from urllib.request import urlopen

# class URLLoader:
#     def create_module(self, target):
#         return None
    
#     def exec_module(self, module):
#         with urlopen(module.__spec__.origin) as page:
#             source = page.read()
#         code = compile(source, module.__spec__.origin, mode="exec")
#         exec(code, module.__dict__)


# Реализация для repl.it
import requests

class URLLoader:
    def create_module(self, target):
        return None
    
    def exec_module(self, module):
        response = requests.get(module.__spec__.origin)
        response.raise_for_status()  # Проверяем успешность запроса
        
        source = response.content
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)
