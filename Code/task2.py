# Task2.py
import task1
import time
import csv


def load_dictionary(hash_table, filename, time_limit):
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

def load_dictionary_time(hash_base, table_size, filename, max_time):
    start_time = time.time()
    # Create new hash table
    X = task1.HashTable(table_size, hash_base)
    try:
        load_dictionary(X, filename, max_time)
    except Exception as e:
        return None, None
    end_time = time.time()
    exe_time = (end_time - start_time)

    if exe_time > max_time:
        return None, None

    return (X.count, exe_time)

def table_load_dictionary_time(max_time):
    filenames = ['english_small.txt','english_large.txt', 'french.txt']
    var = [[1, 250727],[27183,402221],[250726,1000081]]
    # var = [[27183,402221],[250726,1000081]]
    readFile = open('output_task2.csv', 'w')
    readFile.write("%s, %s, %s, %s\n"%('b', 'table_size', 'exe_time', 'filename'))
    for filename in filenames:
        for hase_base, table_size in var:
            (words, exe_time) = load_dictionary_time(hase_base, table_size, filename, max_time)
            if words:
                readFile.write("%d, %d, %.10f, %s\n"%(hase_base, table_size, exe_time, filename))
    readFile.close()


if __name__ == "__main__":
    time_limit = 120
    table_load_dictionary_time(time_limit)