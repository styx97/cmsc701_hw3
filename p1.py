# %% imports 
from rbloom import Bloom
import random
import string 
import time 
from tqdm.auto import tqdm
import pandas as pd

# %%

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
def random_gen_strings(len_start, len_end, total_size):
    """
    Create random strings of length between len_start and len_end
    from the space of characters A, C, T, G
    
    """
    result = []
    sample_len = total_size // ( len_end - len_start ) 
    
    while len(set(result)) < total_size:
        for num in range(len_start, len_end):
            # create a random string of length num sample_len times from the space of A, C, T, G
            for _ in range(sample_len):
                result.append("".join(random.choices(['A', 'C', 'T', 'G'], k=num)))  

    # take a sample of size total_size from the list of strings removing duplicates
    return list(set(result))[:total_size]
        
# %%

random_gen_strings(4, 8, 10)
# %%
powers_of_two = [1/2**i for i in [7,8,10]]
random_strings = [list(random_gen_strings(10, 100, 1000)),
                    list(random_gen_strings(10, 100, 10000)), 
                    list(random_gen_strings(10, 100, 50000)),
                    list(random_gen_strings(10, 100, 100000))]
# %%
# make new sets of string that overlap with the previous sets
new_strings = [[] for _ in range(len(random_strings))]
overlap = []
for i in range(0, len(random_strings)):
    len_key_list = len(random_strings[i])
    
    new_strings[i] = random_strings[i][:len_key_list//2] + list(random_gen_strings(10, 100, len_key_list//2))
    random.shuffle(new_strings[i])
    overlap.append(len(set(new_strings[i]).intersection(set(random_strings[i])))) 

# %%
def get_results(powers_of_two, key_list, query_list):
    
    for keys, queries in zip(key_list, query_list):
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
            
            for index, elem in enumerate(queries) : 
                if elem in keys and results[index] == False:
                    temp_dict['false_negative'] += 1
                elif elem not in keys and results[index] == True:
                    temp_dict['false_positive'] += 1

            temp_dict['query_time'] = query_end_time - query_start_time
            temp_dict['size_in_bits'] = bf.bloom.size_in_bits
    

            print(temp_dict)

    
# %%
results = get_results(powers_of_two, random_strings, new_strings)


# %%
if __name__ == "__main__":



    keys = ["ACTG", "ACT", "ATGT", "ACGGT", "ACT"]
    keys_ = ["ACTG", "ATT", "AGGT", "ACGGT", "ACT", "AGT"]

    bf = BloomFilter(keys, 0.01)

    for elem in keys_: 
        print(elem, elem in keys, bf.query([elem])) 



# %%
keys = ["ACTG", "ACT", "ATGT", "ACGGT", "ACT"]
keys_ = ["ACTG", "ATT", "AGGT", "ACGGT", "ACT", "AGT"]

bf = BloomFilter(keys, 0.01)

for elem in keys_: 
    print(elem, elem in keys, bf.query([elem])) 

# %%
bf = Bloom(100, 0.01)
bf.update(["ACTG", "ACT", "ATGT", "ACGGT", "ACT"])
# %%
