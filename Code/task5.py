#!/usr/bin/env python3
import time
from bst import BinaryTreeNode, BinarySearchTree
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
        self.collision_count = 0
        self.probe_total = 0
        self.probe_max = 0
  
    # This function is the called when we have something like
    # x['abc']
    def __getitem__(self, key):
        # This hash function will find the hash key
        hashed_key = self.hash(key)
        # This is if the there is None
        if self.table[hashed_key] is None:
            # if key have None value then return Exception
            raise KeyError
        else:
            if key in self.table[hashed_key]:
                return self.table[hashed_key][key]
            else:
                KeyError

    # This function will be called when we have something like
    # x['abc'] = 5
    # So this function will set the value at given key
    def __setitem__(self, key, item):
        # Count defines the number of keys have been uploaded to the Hash Table
        self.count += 1
        # Find out the Hash key
        hashed_key = self.hash(key)
        node = self.table[hashed_key]

        probe = 0
        # If the entry is empty
        if node is None:
            # Store the key and the item in tuple format
            my_tree = BinarySearchTree()
            my_tree[key] = item
            self.table[hashed_key] = my_tree
        else: 
            self.collision_count += 1
            self.table[hashed_key][key] = item
            probe = len(self.table[hashed_key])-1
        if probe > self.probe_max:
            self.probe_max = probe

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
    
    # Make the statistics
    def statistics(self):
        for i in range(len(self.table)):
            if self.table[i] is not None  :
                if len(self.table[i]) > 1:
                    self.probe_total = self.probe_total + len(self.table[i]) -1

        return (self.collision_count, self.probe_total, self.probe_max, 0)

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
    return (X.count, exe_time, X.collision_count, X.probe_total, X.probe_max , 0)

def table_load_dictionary_statistics(max_time):
    # Load all the three files
    filenames = ['english_small.txt','english_large.txt', 'french.txt']
    var = [[1, 250727],[27183,402221],[250726,1000081]]
    # var = [[27183,402221],[250726,1000081]]
    # Create new csv file which have all the output for each file
    readFile = open('output_task5.csv', 'w')
    # Store format : 'b', 'table_size', 'exe_time', 'filename'
    readFile.write("%s, %s, %s, %s, %s, %s, %s,\n"%('b', 'table_size', 'exe_time', 'filename', 'collision_count', 'total_probe', 'max_probe'))

    # Iteration over each files
    for filename in filenames:
        for hase_base, table_size in var:
            # Run load_dictionary_time for each file
            (words, exe_time, collision, tp, pm, _) = load_dictionary_statistics(hase_base, table_size, filename, max_time)
            if words:
                # Write all the data according to store format
                readFile.write("%d, %d, %.10f, %s, %d, %d, %d, \n"%(hase_base, table_size, exe_time, filename, collision, tp, pm))
            
    
    # Close the reading file
    readFile.close()
if __name__ == "__main__":
    table_load_dictionary_statistics(120)

    lines = [[1, 250727, 3.0030033588, 'english_small.txt', 82518, 82518, 1], 
    [27183, 402221, 0.6119661331, 'english_small.txt', 8245, 8245, 1], 
    [250726, 1000081, 0.6240065098, 'english_small.txt', 3431, 3431, 1], 
    [1, 250727, 20.6851089001, 'english_large.txt', 192641, 192641, 1], 
    [27183, 402221, 1.6680266857, 'english_large.txt', 40297, 40297, 1], 
    [250726, 1000081, 1.4710021019, 'english_large.txt', 17540, 17540, 1], 
    [1, 250727, 10.9779973030, 'french.txt', 198901, 198901, 1], 
    [27183, 402221, 1.7420518398, 'french.txt', 43261, 43261, 1], 
    [250726, 1000081, 1.6560001373, 'french.txt', 18981, 18981, 1]] 

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

