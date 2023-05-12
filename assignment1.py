# %% 
from rbloom import Bloom
import random
import string 
import time 
from tqdm.auto import tqdm
import pandas as pd
import numpy as np
from utils import prepare_data
from utils import prepare_data_with_overlap


class BloomFilter: 
    def __init__(self, keys: list, error_rate: float):
        self.max_items = len(keys)
        self.error_rate = error_rate
        self.bloom = Bloom(self.max_items, error_rate)
        self.bloom.update(keys)

    def query(self, keys: list) -> bool:
        # return True if all keys are in the bloom filter
        return [key in self.bloom for key in keys]
    
# %%

fractions = [0.3, 0.5, 0.8]

#powers_of_two, key_datasets, query_datasets, overlaps = prepare_data()

    
# %%

for fraction in fractions: 
    print("Fraction of overlap: ", fraction)

    powers_of_two, key_datasets, query_datasets, overlaps = prepare_data_with_overlap(fraction_overlap=fraction) 


    for keys, queries in zip(key_datasets, query_datasets):
        print(f"Key size {len(keys)}, Query size {len(queries)}")
            
        for error_rate in tqdm(powers_of_two):
            temp_dict = {}
            print(f"Error rate {error_rate}")
            
            bf = BloomFilter(keys, error_rate)
            query_start_time = time.time()
            results = bf.query(queries)
            query_end_time = time.time()
            temp_dict['query_size'] = len(queries)
            temp_dict['error_rate'] = error_rate
            temp_dict['false_positive'] = 0
            temp_dict['false_negative'] = 0
            unseen = 0

            for index, elem in enumerate(queries) : 
                if elem in keys and not results[index]: 
                    temp_dict['false_negative'] += 1

                elif elem not in keys : 
                    unseen += 1
                    if results[index] == True:
                        temp_dict['false_positive'] += 1
            
            temp_dict['false_positive_rate'] = temp_dict['false_positive'] / unseen

            temp_dict['query_time'] = query_end_time - query_start_time
            temp_dict['size_in_bits'] = bf.bloom.size_in_bits


            print(temp_dict)
        

# %%
