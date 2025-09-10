import re
import sys
from urllib.request import urlopen


def url_hook(some_str):
      
    if not some_str.startswith(("http", "https")):
        raise ImportError
    with urlopen(some_str) as page: # requests.get()
        data = page.read().decode("utf-8")
    filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
    modnames = {name[:-3] for name in filenames}
    return URLFinder(some_str, modnames)


sys.path_hooks.append(url_hook)
print(sys.path_hooks)