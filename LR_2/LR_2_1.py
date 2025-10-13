import functools
import itertools

def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res
        
def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)
        
        return gen
    return inner 

@fib_coroutine
def my_genn():
    """Сопрограмма"""

    fib_gen = fib_elem_gen()
    fib_list = None

    while True:
        number_of_fib_elem = yield fib_list
        fib_list = list(itertools.islice(fib_gen, number_of_fib_elem))
        



# if __name__ == "__main__":
#     gen = my_genn()
#     print(gen.send(0))
