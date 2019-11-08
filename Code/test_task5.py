import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task5

# Check whether exactly used_cells are occupied.
def check_layout(hash_table, used_cells):
  for (index, cell) in enumerate(hash_table.table):
    if (cell is not None) and (index not in used_cells):
      return False
  return True

class TestTask5(TestCase):
  def test_layout(self):
    with self.vis():
      t = task5.HashTable(128, 1)
      for key in ['ad', 'da']:
        t[key] = 1
      self.assertTrue(check_layout(t, { 69 }),
        msg = "Incorrect chaining layout.")
      
    with self.vis():
      t = task5.HashTable(128, 1)
      for key in ['ad', 'ac' ]:
        t[key] = 1
      self.assertTrue(check_layout(t, { 68, 69 }),
        msg = "Incorrect chaining layout.")

  def test_statistics(self):
    with self.vis():
      t = task5.HashTable(128, 1) 
      for key in ['ad', 'ac', 'ca']:
          t[key] = 1
      self.assertEqual(t.statistics(),
        (1, 1, 1, 0),
        "Incorrect statistics count.")

    with self.vis():
      t = task5.HashTable(128, 1) 
      for key in ['ac', 'bb', 'ca']:
          t[key] = 1
      self.assertEqual(t.statistics(), (2, 2, 2, 0),
        "Incorrect collision count.")

    assert self.check_okay("statistics")


   # Functionality tests are again the same as task 1.
  def test_contains(self):
    x = task5.HashTable(1024, 1)

    with self.vis():
      self.assertFalse("abcdef" in x, "False positive in __contains__ for empty table.")

    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None
      x["abdcef"] = "abcdef"
    
    for key in ["abcdef", "definitely a string", "abdcef"]:
      with self.vis():
        self.assertTrue(key in x, "False negative in __contains__ for key {}".format(key))

    assert self.check_okay("contains")

  def test_getitem(self):
    x = task5.HashTable(1024, 1)

    with self.vis():
      with self.assertRaises(KeyError, msg="x[key] should raise KeyError for missing key."):
        elt = x["abcdef"]
      
    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None

    with self.vis():
      self.assertEqual(x["abcdef"], 18, msg = "Read after store failed.")
    assert self.check_okay("getitem")

  def test_load_2(self):
    " Here, another file is opended and there are 5 lines. "
    with self.vis():
      table = task5.HashTable()
      task5.load_dictionary(table, "words_perm.txt", 10)
      self.assertEqual(count_nonempty_buckets(table), 5)
    self.assertTrue(self.check_okay("load_dictionary"))


  def test_load_timeout(self):
    "Load without time will use the default value of the time out"
    "Default value of the time out is 120 (2 Seconds)"
    with self.vis("load without max_time"):
      table = task5.HashTable()
      task5.load_dictionary(table, "words_simple.txt")

    with self.vis("failed to apply timeout"):
      table = task5.HashTable(100000, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
          self.with_deadline(3, task5.load_dictionary, (table, "english_small.txt", 1))


    # Check with small 500, size
    with self.vis("failed to apply timeout"):
      table = task5.HashTable(500, 1)
      with self.assertRaises(Exception, msg = "reading too many words should time out."):
          self.with_deadline(3, task5.load_dictionary, (table, "english_small.txt", 1))


  # Test load time function
  def test_load_time(self):
    # Test for the words_simple
    (words, time, _, _, _, _) = self.with_deadline(1, task5.load_dictionary_statistics, (31, 100, "words_simple.txt", 10))
    self.assertEqual(words, 6)
    # Test for the words_empty
    (words, time, _, _, _, _) = self.with_deadline(1, task5.load_dictionary_statistics, (31, 100, "words_empty.txt", 10))
    self.assertEqual(words, 11)

  # Test test_table_load_dictionary_time
  def test_table_load_dictionary_time(self):
    task5.table_load_dictionary_statistics(5)
    self.assertTrue(self.check_okay("table_load_dictionary_time"))
if __name__ == '__main__':
  unittest.main()
