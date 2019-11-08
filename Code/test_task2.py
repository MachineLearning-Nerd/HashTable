import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task1
import task2

class TimedOutExn_(Exception):
  def __enter__(self):
    raise TimeoutError

class TestTask2(TestCase):
  def test_load_1(self):
    " This test case load two text file and check for the number of data is loaded"
    # First Test Case
    with self.vis():
      table = task1.HashTable()
      task2.load_dictionary(table, "words_simple.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 6)

    # Second Test case
    with self.vis():
      table = task1.HashTable()
      task2.load_dictionary(table, "words_empty.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 11, "Failed to handle empty line or whitespace.")

    self.assertTrue(self.check_okay("load_dictionary"))

  def test_load_2(self):
    " Here, another file is opended and there are 5 lines. "
    with self.vis():
      table = task1.HashTable()
      task2.load_dictionary(table, "words_perm.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 5)
    self.assertTrue(self.check_okay("load_dictionary"))

  def test_load_timeout(self):
    "Load without time will use the default value of the time out"
    "Default value of the time out is 120 (2 Seconds)"
    # First test case
    with self.vis("load without max_time"):
      table = task1.HashTable()
      task2.load_dictionary(table, "words_simple.txt")

    # Second test case
    with self.vis("failed to apply timeout"):
      table = task1.HashTable(100000, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
        try:
          self.with_deadline(3, task2.load_dictionary, (table, "english_small.txt", 1))
        except TimedOutExn_:
          print("Taking large time")


    # Third test case
    # Check with small 500, size
    with self.vis("failed to apply timeout"):
      table = task1.HashTable(500, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
        try:
          self.with_deadline(3, task2.load_dictionary, (table, "english_small.txt", 1))
        except TimedOutExn_:
          print("Taking large time")

    self.assertTrue(self.check_okay("load_dictionary timeout"))

  # Test load time function
  def test_load_time(self):
    # First Test case
    with self.vis("reporting words"):
      (words, time) = self.with_deadline(1, task2.load_dictionary_time, (31, 100, "words_simple.txt", 10))
      self.assertEqual(words, 6)

    # Second Test case
    with self.vis("reporting words"):
      (words, time) = self.with_deadline(1, task2.load_dictionary_time, (31, 100, "words_empty.txt", 10))
      self.assertEqual(words, 11)
    self.assertTrue(self.check_okay("load_dictionary time"))

  # Test test_table_load_dictionary_time
  def test_table_load_dictionary_time(self):
    task2.table_load_dictionary_time(5)
    self.assertTrue(self.check_okay("table_load_dictionary_time"))


if __name__ == '__main__':
  unittest.main()
