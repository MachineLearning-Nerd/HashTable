#!/usr/bin/env python3
"""
:author: Graeme Gange
"""

class HashTable:
    # This is the __init__ function
    def __init__(self, table_capacity=1024, hash_base=17): 
        # It have default lengh of table_capacity and hash_bash
        self.table = [None] * table_capacity
        # This variable shows the maximum length
        self.max_length = table_capacity
        self.base = hash_base
        self.count = 0
  
    # This function is the called when we have something like
    # x['abc']
    def __getitem__(self, key):
        # This hash function will find the hash key
        hashed_key = self.hash(key)
        if self.table[hashed_key] is None:
            # if key have None value then return Exception
            raise KeyError
        if self.table[hashed_key][0] != key:
            # If the key is not at the hashed_key
            original_key = hashed_key
            # This is done because we have used the linear Probing 
            while self.table[hashed_key][0] != key:
                # Find out the new hashed_key for linear probing
                hashed_key = (hashed_key + 1) % self.max_length 
                if self.table[hashed_key] is None:
                    raise KeyError
                if hashed_key == original_key:
                    raise KeyError
        return self.table[hashed_key][1]

    # This function will be called when we have something like
    # x['abc'] = 5
    # So this function will set the value at given key
    def __setitem__(self, key, item):
        # Count defines the number of keys have been uploaded to the Hash Table
        self.count += 1
        # Find out the Hash key
        hashed_key = self.hash(key)
        while self.table[hashed_key] is not None:
            if self.table[hashed_key][0] == key:
                self.count -= 1
                break
            hashed_key = (hashed_key + 1) % self.max_length 
        # Store the key and the item in tuple format
        keytuple = (key, item)
        self.table[hashed_key] = keytuple
        # If the lsit is full then go to this function
        if self.count / float(self.max_length) >= 1:
            self.rehash()

    # This function will be called when we have something like 
    # 'abc' in x
    # This function will return True or False
    def __contains__(self, key):
        # If the Hash table have that key then it will return True
        try:
            self.__getitem__(key)
            return True 
        # Other wise it will return False
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

    # This function will be called when Hash table is full and 
    # We want to insert the data
    def rehash(self):
        # This is the list of the prime number given in the assignment
        Primes = [ 3, 7, 11, 17, 23, 29, 37, 47, 59, 71, 89, 107, 131, 163, 197, 239, 293, 353, 431, 521, 631, 761,
                    919, 1103, 1327, 1597, 1931, 2333, 2801, 3371, 4049, 4861, 5839, 7013, 8419, 10103, 12143, 14591,
                    17519, 21023, 25229, 30313, 36353, 43627, 52361, 62851, 75521, 90523, 108631, 130363, 156437,
                    187751, 225307, 270371, 324449, 389357, 467237, 560689, 672827, 807403, 968897, 1162687, 1395263,
                    1674319, 2009191, 2411033, 2893249, 3471899, 4166287, 4999559, 5999471, 7199369]
        # Find out the prime number which is larger then the double
        # of the length of the current table
        nlength = 0 
        for val in Primes:
            if val < 2 * self.max_length:
                continue
            else: 
                nlength = val
                break
        # Raise the value error when the newlenght is not in the prime number list
        if nlength == 0:
            raise ValueError

        self.max_length = nlength
        self.count = 0
        # Store old table
        old_table = self.table
        self.table = [None] * self.max_length
        # Create new table with increased size
        for keytuple in old_table:
            if keytuple is not None:
                self[keytuple[0]] = keytuple[1]