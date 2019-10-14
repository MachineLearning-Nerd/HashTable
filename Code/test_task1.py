import sys
from contextlib import contextmanager
import math
import unittest
from test_common import *
import task1

class TestTask1(TestCase):
  def test_init(self):
    with self.vis("empty init"):
      x = task1.HashTable()
    with self.vis("init with size and base"):
      z = task1.HashTable(800, 2398)
      
    assert self.check_okay("init")
    
  def test_hash(self):

    x = task1.HashTable(1024, 17)
    for (key, expect) in [("", 0),
                          ("abcdef", 389),
                          ("defabc", 309)]:
        with self.vis():
          self.assertEqual(x.hash(key), expect, msg=f"Unexpected hash with base 17 and key {key}.")

    assert self.check_okay("hash")

  # The tests for __contains__ and __getitem__ use __setitem__, so we don't make any assumptions
  # about the underlying array representation. Remember to define your own tests for __setitem__
  # (and rehash)
  def test_contains(self):
    x = task1.HashTable(1024, 1)

    with self.vis():
      self.assertFalse("abcdef" in x, "False positive in __contains__ for empty table.")

    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None
      x["abdcef"] = "abcdef"
    
    # Check for the Ture condition
    for key in ["abcdef", "definitely a string", "abdcef"]:
      with self.vis():
        self.assertTrue(key in x, "False negative in __contains__ for key {}".format(key))

    # Check False condition
    with self.vis():
      self.assertEqual("key" in x, False, msg = "contains failed.")

    assert self.check_okay("contains")

  def test_getitem(self):
    x = task1.HashTable(1024, 1)

    with self.vis():
      with self.assertRaises(KeyError, msg="x[key] should raise KeyError for missing key."):
        elt = x["abcdef"]
      
    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None
    with self.vis():
      self.assertEqual(x["abcdef"], 18, msg = "Read after store failed.")

    x["abdcef"] = 22
    with self.vis():
      self.assertEqual(x["abdcef"], 22, msg = "Read after store failed.")

    assert self.check_okay("getitem")

  # Test for the set items
  def test_setitems(self):
    x = task1.HashTable(1024, 1)

    # Set 2 values 
    with self.vis("unexpected failure in setitem"):
      x["abcdef"] = 18
      x["definitely a string"] = None
      
    # Check wether 2 items are set properly or not
    assert x.count == 2

    # Check for each value
    with self.vis():
      self.assertEqual(x["abcdef"], 18, msg = "Read after store failed.")
    with self.vis():
      self.assertEqual(x["definitely a string"], None, msg = "Read after store failed.")

    # Set one more item
    x["abdcef"] = 22

    assert x.count == 3
    assert self.check_okay("setitem")

  # Test rehash 
  def test_rehash_1(self):
    # This test case will test for different length
    # Here length is 3 so new length should be grater then 2*old_length
    # So here it should be 7

    x = task1.HashTable(3,3)
    x['abc'] = 1
    x['abd'] = 2
    x['abe'] = 3
    x['abf'] = 4
    
    assert x.max_length == 7 
    assert self.check_okay("rehash")

  def test_rehash_2(self):
    # This test case will test for different length
    # Here length is 5 so new length should be grater then 2*old_length
    # So here it should be 11
    x = task1.HashTable(5,3)
    x['abc'] = 1
    x['abd'] = 2
    x['abe'] = 3
    x['abf'] = 4
    x['abg'] = 5
    assert x.max_length == 11 
    assert self.check_okay("rehash")

if __name__ == '__main__':
  unittest.main()
