from setuptools import setup
from io import open

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='bin_tree_chikina',
      version='0.0.2',
      description='Python module for build been tree',
      packages=['bin_tree_chikina'],
      author_email='arin.tchikina@yandex.ru',
      author = 'ChikinaAO',
      long_description = long_description,
      long_description_content_type='text/markdown',
      url = 'https://github.com/chikKik/Python-lab-3nd-course/tree/main/LR_3',
      zip_safe=False)