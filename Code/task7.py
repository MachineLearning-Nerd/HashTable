#!/usr/bin/env python3
"""
:author: Graeme Gange
"""

from task1 import HashTable
import re
class NewHashTable(HashTable):
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
        if self.count / float(self.max_length) >= 0.5:
            self.rehash()

class Freq:
    def __init__(self, table_size=1000081, hase_base=250726):
        self.word_frequency = NewHashTable(table_size, hase_base)
        # This variable will take care of max occurance of word
        self.max_fre = 0
        # This will kep trake of that maximum occured word
        self.max_word =''
  
    def add_file(self, filename):
        # This line will open the filename
        f = open(filename,"r", encoding='utf-8')
        # This line will read the lines
        lines = f.readlines()
        # This will close the file
        f.close()

        for i, line in enumerate(lines):
            line = line.strip('\n')
            # This line will remove the Punctuation
            line = re.sub(r'[^\w\s]', '', line)
            # Split the lines into words
            words = line.split(' ')
            for word in words:
                # This just to make sure that "The" and "the" are not different
                word = word.lower()

                # Make sure that list is not empty
                if word != '' :
                    # if word exist and increment by one
                    if word in self.word_frequency:
                        self.word_frequency[word] = self.word_frequency[word] + 1
                    # If not then create that word and assign it to one
                    else:
                        self.word_frequency[word] = 1
                    # This is to findout the max_fre and max_word
                    val = self.word_frequency[word]
                    if val > self.max_fre:
                        self.max_fre = val 
                        self.max_word = word 


    def rarity(self, word):
        # make "The" to 'the'
        word = word.lower()
        if word in self.word_frequency:
            # Find out the frequency
            val = self.word_frequency[word]
            if val >= (self.max_fre/100):
                return 0
            elif val  <= (self.max_fre/1000):
                return 2
            elif val  >= (self.max_fre/1000) and val < (self.max_fre/100):
                return 1
            else:
                return 3
            # 5 is multiplied just to get the range [0, 5]
            # return (val/self.max_fre) * 5
        else:
            return 3
            # If word is not exist in the table then keyerror
            # raise KeyError("Wrong key")

    def evaluate_frequency(self, other_filename):
        comman,rare,uncomman,neverused = 0, 0, 0, 0
        # This line will open the filename
        f = open(other_filename,"r", encoding='utf-8')
        # This line will read the lines
        lines = f.readlines()
        # This will close the file
        f.close()

        for i, line in enumerate(lines):
            line = line.strip('\n')
            # This line will remove the Punctuation
            line = re.sub(r'[^\w\s]', '', line)
            # Split the lines into words
            words = line.split(' ')
            for word in words:
                # This just to make sure that "The" and "the" are not different
                word = word.lower()

                # Make sure that list is not empty
                if word != '' :
                    # if word exist and increment by one
                    if word in self.word_frequency:
                        # Find out the frequency
                        val = self.word_frequency[word]
                        if val >= (self.max_fre/100):
                            comman += 1
                        elif val  <= (self.max_fre/1000):
                            rare += 1
                        elif val  >= (self.max_fre/1000) and val < (self.max_fre/100):
                            uncomman += 1
                        else:
                            neverused += 1
                    # If not then create that word and assign it to one
                    else:
                        neverused += 1
        total = comman + uncomman + rare + neverused
        return (comman*100/total, uncomman*100/total, rare*100/total, neverused*100/total)
    def __getitem__(self, word):
        val =  self.rarity(word)
        if val == 0:
            return 'comman'
        elif val == 1:
            return 'rare'
        elif val == 2:
            return 'uncommon'
        elif val == 3:
            return 'misspelling'
                

if __name__ == "__main__":
    # a = Freq(5, 3)
    # a.add_file('mytest_task.txt')
    # print(a.word_frequency.table)
    a = Freq()
    a.add_file('84-0.txt')
    a.add_file('1342-0.txt')
    a.add_file('2600-0.txt')
    val = a.evaluate_frequency('98-0.txt')
    print(a['book'])
    print(val)
    
    # print(a.rarity('the'))
