import unittest
from test_common import *
import task6

class TestTask6(TestCase):
    "Every where I have used 'the' to check the rarity because the is highest occured word."
    def test_add_files_1(self):
        "Here I have just taken a words_empty.txt file to find out the frequency"
        X = task6.Freq()
        X.add_file('words_empty.txt')

        val = X.rarity('and')
        self.assertEqual(val, 0)
        self.assertEqual(X.word_frequency.count, 9)
        with self.assertRaises(KeyError) as context:
            val = X.rarity('rocks')
        self.assertTrue("Wrong key" in str(context.exception))

    "These are the test on all the ebooks that are given"
    def test_add_files_2(self):
        X = task6.Freq()
        X.add_file('84-0.txt')

        # rocks is rare word
        val = X.rarity('rocks')
        self.assertEqual(val, 2)

    def test_add_files_3(self):
        X = task6.Freq()
        X.add_file('98-0.txt')

        # mail is  Uncomman word
        val = X.rarity('mail')
        self.assertEqual(val, 1)

    def test_add_files_4(self):
        X = task6.Freq()
        X.add_file('1342-0.txt')

        val = X.rarity('the')
        self.assertEqual(val, 0)

    def test_add_files_5(self):
        X = task6.Freq()
        X.add_file('2600-0.txt')

        val = X.rarity('the')
        self.assertEqual(val, 0)

if __name__ == '__main__':
  unittest.main()