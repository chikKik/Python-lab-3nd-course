

class FibonacchiLst:
    def __init__(self, lst):
        self.lst = lst
        self.index = 0
        self.fib_seq = self.Fib_gen(max(lst) if lst else 0)# проверка, что lst непустое
        self.fib_num = set()
        self.one = 0# счетчик единиц(тк в послед. Фибоначчи две единицы)


    def Fib_gen(self, n):
        '''Генерация чисел Фибоначчи по максимальному заданному числу.'''
        if n == 0:
            return [0]

        fib_seq = [0, 1]
        while True:
            rez = fib_seq[-2] + fib_seq[-1]
            if rez <= n: 
                fib_seq.append(rez)
            else:
                break
        return fib_seq
        

    def __iter__(self):
        return self

    def __next__(self):
            
        while self.index < len(self.lst):
            fib_current = self.lst[self.index]
            self.index += 1

            if fib_current in self.fib_seq:# проверка, содержится ли число в послед. Фибоначчи
                if fib_current == 1:# проверка на количество единиц в последовательности
                    if self.one < 2:
                        self.one += 1
                        return fib_current
                    else:
                        continue# пропускает лишнюю единицу

                if fib_current not in self.fib_num:# не дает пройти повторяющимся числам, кроме единиц
                    self.fib_num.add(fib_current)
                    return fib_current

        raise StopIteration
        

# print(list(FibonacchiLst([1, 1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 0])))