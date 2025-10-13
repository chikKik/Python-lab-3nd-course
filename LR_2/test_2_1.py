import LR_2_1
import unittest


class TestStringMethods(unittest.TestCase):

    def test_5_el(self):
        gen = LR_2_1.my_genn()
        self.assertEqual(gen.send(5), [0, 1, 1, 2, 3])##assertEqual() для проверки ожидаемого результата

    def test_1_el(self):
        gen = LR_2_1.my_genn()
        self.assertEqual(gen.send(1), [0])

    def test_0_el(self):
        gen = LR_2_1.my_genn()
        self.assertEqual(gen.send(0), [])
        
    def test_7_el(self):
        gen = LR_2_1.my_genn()
        self.assertEqual(gen.send(7), [0, 1, 1, 2, 3, 5, 8])

    def test_15_el(self):
        gen = LR_2_1.my_genn()
        self.assertEqual(gen.send(15), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377])
unittest.main()