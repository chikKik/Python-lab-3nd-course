# В URLFinder и будет срабатывать функция url_hook, которая и будет перехватывать ситуацию, в которой загрузка модуля 
# должна идти по URL-адресу

from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available
        
    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)
        
        else:
            return None