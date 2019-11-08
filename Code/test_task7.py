import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task7

class TestTask6(TestCase):
    "Every where I have used 'the' to check the rarity because the is highest occured word."
    def test_add_files_1(self):
        "Here I have just taken a words_empty.txt file to find out the frequency"
        X = task7.Freq()
        X.add_file('words_empty.txt')

        val = X.rarity('and')
        self.assertEqual(val, 0)
        self.assertEqual(X.word_frequency.count, 9)

        val = X.rarity('rocks')
        self.assertEqual(val, 3)

        val = X.evaluate_frequency('98-0.txt')
        self.assertEqual(len(val), 4)


    def test_add_files_2(self):
        "Here I have just taken a words_empty.txt file to find out the frequency"
        X = task7.Freq()
        X.add_file('84-0.txt')

        val = X.evaluate_frequency('98-0.txt')
        self.assertEqual(len(val), 4)

    def test_add_files_4(self):
        X = task7.Freq()
        X.add_file('84-0.txt')

        val = X.evaluate_frequency('1342-0.txt')
        self.assertEqual(len(val), 4)

    def test_add_files_5(self):
        X = task7.Freq()
        X.add_file('84-0.txt')

        val = X.evaluate_frequency('2600-0.txt')
        self.assertEqual(len(val), 4)
    
    def test_getitem(self):
        a = task7.Freq()
        a.add_file('84-0.txt')
        a.add_file('1342-0.txt')
        a.add_file('2600-0.txt')
        val = a.evaluate_frequency('98-0.txt')
        r = a['book']
        self.assertEqual(r,'rare')

if __name__ == '__main__':
  unittest.main()