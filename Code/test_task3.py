import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task3

class TestTask3(TestCase):
  def test_statistics(self):
    table = task3.HashTable(1024, 1)

    # First Test Statistics
    with self.vis("testing statistics"):
      for key in ["abcdef", "defabc"]:
        table[key] = 1
      stats = table.statistics()

    # Second Test Statistics
    with self.vis():
      for key in ["acbedf"]:
        table[key] = 1
      stats = table.statistics()
      self.assertEqual(stats, (2, 3, 2, 0), "incorrect statistics")

    self.assertTrue(self.check_okay("statistics"))

  def test_load_statistics(self):

    # First Test case
    with self.vis("reporting words"):
      (w, _, _, _, _, _) = self.with_deadline(1, task3.load_dictionary_statistics, (1, 1024, "words_perm.txt", 10))
      self.assertEqual(w, 5, "incorrect word count")

    # Second Test case
    with self.vis("reporting words"):
      (w, _, _, _, _, _) = self.with_deadline(1, task3.load_dictionary_statistics, (1, 1024, "words_empty.txt", 10))
      self.assertEqual(w, 11, "incorrect word count")

    self.assertTrue(self.check_okay("load_statistics"))

  def test_load_2(self):
    " Here, another file is opended and there are 5 lines. "
    with self.vis():
      table = task3.HashTable()
      task3.load_dictionary(table, "words_perm.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 5)

    with self.vis():
      table = task3.HashTable()
      task3.load_dictionary(table, "words_empty.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 11)
    self.assertTrue(self.check_okay("load_dictionary"))


  def test_load_timeout(self):
    "Load without time will use the default value of the time out"
    "Default value of the time out is 120 (2 Seconds)"
    with self.vis("load without max_time"):
      table = task3.HashTable()
      task3.load_dictionary(table, "words_simple.txt")

    with self.vis("failed to apply timeout"):
      table = task3.HashTable(100000, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
          self.with_deadline(3, task3.load_dictionary, (table, "english_small.txt", 1))


    # Check with small 500, size
    with self.vis("failed to apply timeout"):
      table = task3.HashTable(500, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
          self.with_deadline(3, task3.load_dictionary, (table, "english_small.txt", 1))


  # Test load time function
  def test_load_time(self):
    # Test for the words_simple
    (words, time, _, _, _, _) = self.with_deadline(1, task3.load_dictionary_statistics, (31, 100, "words_simple.txt", 10))
    self.assertEqual(words, 6)
    # Test for the words_empty
    (words, time, _, _, _, _) = self.with_deadline(1, task3.load_dictionary_statistics, (31, 100, "words_empty.txt", 10))
    self.assertEqual(words, 11)

  # Test test_table_load_dictionary_time
  def test_table_load_dictionary_time(self):
    task3.table_load_dictionary_statistics(5)
    self.assertTrue(self.check_okay("table_load_dictionary_time"))
if __name__ == '__main__':
  unittest.main()
