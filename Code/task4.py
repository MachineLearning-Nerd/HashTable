#!/usr/bin/env python3
import time
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
        self.rehash_count = 0
        self.collision_count = 0
        self.probe_total = 0
        self.probe_max = 0
        self.pre_prob = 0
  
    # This function is the called when we have something like
    # x['abc']
    def __getitem__(self, key):
        # This hash function will find the hash key
        hashed_key = self.hash(key)
        if self.table[hashed_key] is None:
            # if key have None value then return Exception
            raise KeyError
        probe = 1
        if self.table[hashed_key][0] != key:
            # If the key is not at the hashed_key
            original_key = hashed_key
            # This is done because we have used the linear Probing 
            while self.table[hashed_key][0] != key:
                # Find out the new hashed_key for linear probing
                hashed_key = (hashed_key + probe*probe) % self.max_length 
                probe += 1
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
        old_hashed_key = hashed_key
        if self.table[hashed_key] is not None:
            self.collision_count += 1
        probe = 1
        while self.table[hashed_key] is not None:
            if self.table[hashed_key][0] == key:
                self.count -= 1
                break
            hashed_key = (old_hashed_key + probe*probe) % self.max_length 
            probe += 1
            self.probe_total += 1
        
        if probe-1 > self.probe_max :
            # print(probe)
            self.probe_max = probe-1

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
        self.rehash_count += 1
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

    
    # Make the statistics
    def statistics(self):
        return (self.collision_count, self.probe_total, self.probe_max, self.rehash_count)



def load_dictionary(hash_table, filename, time_limit=120):
    """ hash_table is the instance from the task 1,
        filename is the name of the txt file, 
        time_limit is the limit for execution.
        Make sure that time_limit should in minutes. 
    """
    start_time = time.time()
    # This line will open the filename
    f = open(filename,"r", encoding='utf-8')
    # This line will read the lines
    lines = f.readlines()
    # This will close the file
    f.close()
    for ind, line in enumerate(lines): 
        # Add the word from the line after removing space and the \n character
        # hash_table[line.strip('\n').strip(' ')] = 1
        try:
            hash_table[line] = 1
        except Exception as e:
            print(str(e))

        # Find out the time
        mid_time = time.time()
        # if time taken to load the file in the dictionary is much more than the time limit
        # then raise the TimeoutError
        if mid_time - start_time > time_limit:
            raise TimeoutError

def load_dictionary_statistics(hash_base, table_size, filename, max_time):
    start_time = time.time()
    # Create new hash table
    X = HashTable(table_size, hash_base)
    try:
        # Loas the dictionary
        load_dictionary(X, filename, max_time)
    except Exception as e:
        # If there is timeout error then return None
        return [None] * 6
    
    # Findout the execution time
    end_time = time.time()
    exe_time = (end_time - start_time)

    # If execution time is greater than the maxtime then 
    # return None, None
    if exe_time > max_time:
        return [None] * 6

    # print(X.count, exe_time, X.collision_count, X.probe_total, X.probe_max, X.rehash_count)
    return (X.count, exe_time, X.collision_count, X.probe_total, X.probe_max, X.rehash_count)

def table_load_dictionary_statistics(max_time):
    # Load all the three files
    filenames = ['english_small.txt','english_large.txt', 'french.txt']
    var = [[1, 250727],[27183,402221],[250726,1000081]]
    # var = [[27183,402221],[250726,1000081]]
    # Create new csv file which have all the output for each file
    readFile = open('output_task4.csv', 'w')
    # Store format : 'b', 'table_size', 'exe_time', 'filename'
    readFile.write("%s, %s, %s, %s\n"%('b', 'table_size', 'exe_time', 'filename'))

    # Iteration over each files
    for filename in filenames:
        for hase_base, table_size in var:
            # Run load_dictionary_time for each file
            (words, exe_time, collision, tp, pm, rehase_count) = load_dictionary_statistics(hase_base, table_size, filename, max_time)
            if words:
                # Write all the data according to store format
                readFile.write("%d, %d, %.10f, %s, %d, %d, %d, %d,\n"%(hase_base, table_size, exe_time, filename, collision, tp, pm, rehase_count))
            
    
    # Close the reading file
    readFile.close()

if __name__ == "__main__":
    # hash_base, table_size, filename, max_time = 1, 3, 'words_perm.txt', 2
    # load_dictionary_statistics(hash_base, table_size, filename, max_time)
    time_limit = 120
    table_load_dictionary_statistics(time_limit)

    lines = [[1, 250727, 5.2579996586, 'english_small.txt', 83695, 8307882, 399, 0],
    [27183, 402221, 0.4930355549, 'english_small.txt', 8844, 19779, 7, 0],
    [250726, 1000081, 0.4349615574, 'english_small.txt', 3548, 7401, 5, 0],
    [1, 250727, 37.2243041992, 'english_large.txt', 194056, 48586956, 1367, 0],
    [27183, 402221, 1.2400023937, 'english_large.txt', 47011, 125973, 16, 0],
    [250726, 1000081, 1.1790373325, 'english_large.txt', 18656, 41346, 7, 0],
    [1, 250727, 24.7367544174, 'french.txt', 201747, 34671545, 883, 0],
    [27183, 402221, 1.3115441799, 'french.txt', 50918, 138370, 19, 0],
    [250726, 1000081, 1.2770001888, 'french.txt', 20373, 45348, 7, 0]]


    x_label = ['b=1 t=250727', 'b=27183 t=402221', 'b=250726 t=1000081']

    import matplotlib.pyplot as plt
    import numpy as np
    # data to plot
    n_groups = 3
    means_low = (lines[0][4], lines[1][4], lines[2][4])
    means_mid = (lines[3][4], lines[4][4], lines[5][4])
    means_high = (lines[6][4], lines[7][4], lines[8][4])

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2
    opacity = 0.8

    rects1 = plt.bar(index, means_low, bar_width,
    alpha=opacity,
    color='b',
    label='english_small.txt')

    rects2 = plt.bar(index + bar_width, means_mid, bar_width,
    alpha=opacity,
    color='g',
    label='english_large.txt')

    rects2 = plt.bar(index + bar_width *2 , means_high, bar_width,
    alpha=opacity,
    color='r',
    label='french.txt')

    plt.xlabel('Combination')
    plt.ylabel('Collision Count')
    plt.xticks(index + bar_width, x_label)
    plt.legend()

    plt.tight_layout()
    plt.show()


    means_low = (lines[0][2], lines[1][2], lines[2][2])
    means_mid = (lines[3][2], lines[4][2], lines[5][2])
    means_high = (lines[6][2], lines[7][2], lines[8][2])

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2
    opacity = 0.8

    rects1 = plt.bar(index, means_low, bar_width,
    alpha=opacity,
    color='b',
    label='english_small.txt')

    rects2 = plt.bar(index + bar_width, means_mid, bar_width,
    alpha=opacity,
    color='g',
    label='english_large.txt' )

    rects2 = plt.bar(index + bar_width *2 , means_high, bar_width,
    alpha=opacity,
    color='r',
    label='french.txt')

    plt.xlabel('Combination')
    plt.ylabel('Time')
    plt.xticks(index + bar_width, x_label)
    plt.legend()

    plt.tight_layout()
    plt.show()

