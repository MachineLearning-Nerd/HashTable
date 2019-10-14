#!/usr/bin/env python3
"""
:author: Graeme Gange
"""

class HashTable:
    def __init__(self, table_capacity=1024, hash_base=17): 
        self.table = [None] * table_capacity
        self.base = hash_base
        self.count = 0
  
    def __getitem__(self, key):
        key_hash = self.hash(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        else :
            raise  KeyError()

    def __setitem__(self, key, item):
        key_hash = self.hash(key)
        key_value = [key, item] if item != None else [key, str(item)]
        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] =  item
                    return True
            self.table[key_hash].append(key_value)
            return True

    def __contains__(self, key):
        try:
            return self.__getitem__(key) != None
        except Exception as e:
            return False

    def hash(self, key):
        """
            This is to create the hash function.
            This function returns the index for the hash code.
        """
        # Initialize the hash as 0
        hashsum = 0
        for idx, c in enumerate(str(key)):
            # ord returns an integer representing the Unicode 
            # code point for the character
            hashsum = hashsum * self.base + ord(c)
            hashsum = hashsum % len(self.table)
        # Return the index within the hash table size by modulo operator
        return hashsum 

    def rehash(self):
        raise NotImplementedError
