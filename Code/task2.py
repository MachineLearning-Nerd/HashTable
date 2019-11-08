# Task2.py
import task1
import time
import csv


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

def load_dictionary_time(hash_base, table_size, filename, max_time):
    start_time = time.time()
    # Create new hash table
    X = task1.HashTable(table_size, hash_base)
    try:
        # Loas the dictionary
        load_dictionary(X, filename, max_time)
    except Exception as e:
        # If there is timeout error then return None
        return None, None
    
    # Findout the execution time
    end_time = time.time()
    exe_time = (end_time - start_time)

    # If execution time is greater than the maxtime then 
    # return None, None
    if exe_time > max_time:
        return None, None

    return (X.count, exe_time)

def table_load_dictionary_time(max_time):
    # Load all the three files
    filenames = ['english_small.txt','english_large.txt', 'french.txt']
    var = [[1, 250727],[27183,402221],[250726,1000081]]
    # var = [[27183,402221],[250726,1000081]]
    # Create new csv file which have all the output for each file
    readFile = open('output_task2.csv', 'w')
    # Store format : 'b', 'table_size', 'exe_time', 'filename'
    readFile.write("%s, %s, %s, %s\n"%('b', 'table_size', 'exe_time', 'filename'))

    # Iteration over each files
    for filename in filenames:
        for hase_base, table_size in var:
            # Run load_dictionary_time for each file
            (words, exe_time) = load_dictionary_time(hase_base, table_size, filename, max_time)
            if words:
                # Write all the data according to store format
                readFile.write("%d, %d, %.10f, %s\n"%(hase_base, table_size, exe_time, filename))
            
    
    # Close the reading file
    readFile.close()


if __name__ == "__main__":
    time_limit = 120
    table_load_dictionary_time(time_limit)

    lines = [[27183, 402221, 0.4680006504, 'english_small.txt'],
    [250726, 1000081, 0.4640004635, 'english_small.txt'],
    [27183, 402221, 1.0610003471, 'english_large.txt'],
    [250726, 1000081, 1.0419979095, 'english_large.txt'],
    [27183, 402221, 1.2390501499, 'french.txt'],
    [250726, 1000081, 1.2249720097, 'french.txt']]

    x_label = ['b=27183 t=402221', 'b=250726 t=1000081']

    import matplotlib.pyplot as plt
    import numpy as np
    # data to plot
    n_groups = 2
    means_low = (lines[0][2], lines[1][2])
    means_mid = (lines[2][2], lines[3][2])
    means_high = (lines[4][2], lines[5][2])

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.20
    opacity = 0.8

    rects1 = plt.bar(index, means_low, bar_width,
    alpha=opacity,
    color='b',
    label='english_small.txt')

    rects2 = plt.bar(index + bar_width, means_mid, bar_width,
    alpha=opacity,
    color='g',
    label='english_large.txt')

    rects3 = plt.bar(index + bar_width*2, means_high, bar_width,
    alpha=opacity,
    color='r',
    label='french.txt')

    plt.xlabel('Combination')
    plt.ylabel('Execution Time')
    plt.xticks(index + bar_width, x_label)
    plt.legend()

    plt.tight_layout()
    plt.show()
