#!/usr/bin/env python3
"""
:author: Graeme Gange
"""

class HashTable:
    def __init__(self, table_capacity=1024, hash_base=17): 
        self.table = [None] * table_capacity
        self.max_length = table_capacity
        self.base = hash_base
        self.count = 0
  
    def __getitem__(self, key):
        # key_hash = self.hash(key)
        # if self.table[key_hash] is not None:
        #     for pair in self.table[key_hash]:
        #         if pair[0] == key:
        #             return pair[1]
        # else :
        #     raise  KeyError()
        hashed_key = self.hash(key)
        if self.table[hashed_key] is None:
            raise KeyError
        if self.table[hashed_key][0] != key:
            original_key = hashed_key
            while self.table[hashed_key][0] != key:
                hashed_key = (hashed_key + 1) % self.max_length # self._increment_key(hashed_key)
                if self.table[hashed_key] is None:
                    raise KeyError
                if hashed_key == original_key:
                    raise KeyError
        
        return self.table[hashed_key][1]

    def __setitem__(self, key, item):
        # key_hash = self.hash(key)
        # key_value = [key, item] if item != None else [key, str(item)]
        # if self.table[key_hash] is None:
        #     self.table[key_hash] = list([key_value])
        #     return True
        # else:
        #     for pair in self.table[key_hash]:
        #         if pair[0] == key:
        #             pair[1] =  item
        #             return True
        #     self.table[key_hash].append(key_value)
        #     return True
        self.count += 1
        hashed_key = self.hash(key)
        while self.table[hashed_key] is not None:
            if self.table[hashed_key][0] == key:
                self.count -= 1
                break
            hashed_key = (hashed_key + 1) % self.max_length #self._increment_key(hashed_key)
        keytuple = (key, item)
        self.table[hashed_key] = keytuple
        if self.length / float(self.max_length) >= 1:
            self.rehash()

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
