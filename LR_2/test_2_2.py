import LR_2_2_Fibonachi
import unittest


class TestStringMethods(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0])), [1, 1, 2, 3, 5, 8, 0])##assertEqual() для проверки ожидаемого результата

    def test_duplicate(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([1, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 0])), [1, 1, 2, 3, 5, 8, 0])

    def test_ones(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([1, 1, 1, 1, 1])), [1, 1])
        
    def test_non_fib(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([4, 1, 6, 2, 7, 3, 8, 9, 1, 5, 1])), [1, 2, 3, 8, 1, 5])

    def test_single(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([3])), [3])
    
    def test_zero(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([0, 0])), [0])

    def test_negative(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([1, 3, -5])), [1, 3])
    
    def test_float(self):
        self.assertEqual(list(LR_2_2_Fibonachi.FibonacchiLst([1.0, 3.0, 5.0, 7.0])), [1.0, 3.0, 5.0])
unittest.main()