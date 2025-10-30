'''Построение бинарного дерева с помошью рекурсии'''

class BinTree(Exception):
    '''Класс для обработки исключений'''
    pass

def bin_tree(root=1, height=5, left_way = lambda x: x*2, right_way = lambda y: y+3 ):
    '''
    Функция рекурсии, углубляется и одновременно вычиляет значения корней
    Аргументы:
    root(int)-корень, изменяющееся знач.
    height(int)-высота, уменьшается с каждым циклом
    left_way(func)- анонимная функция, задает условие для левого потомка
    right_way(func)- анонимная функция, задает условие для правого потомка
    
    Возвращает: либо 0, либо словарь, содержащий всех потомков root попарно. Внутри словаря происходит рекурсивный вызов функции
    '''
    if not isinstance(height, int) or height < 0:
        raise BinTree("Высота дерева должна быть неотрицательным и целым числом")
    
    if not isinstance(root, int):
        raise BinTree("В корне дерева должно быть целое число")
    

    if height == 0: #условие выхода из рекурсии
        return 0

    try:
       return {root: [bin_tree(left_way(root), height-1), bin_tree(right_way(root), height-1)]}
    
    except Exception as e:
        raise BinTree(f'Найдена ошибка при построении бинарного дерева: {e}')
