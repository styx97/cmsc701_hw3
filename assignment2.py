# %% 
import random
from collections import defaultdict
# %% 
import time 
import bbhash 
import os 
from tqdm.auto import tqdm 
from bbhash_table import BBHashTable
from utils import prepare_data, prepare_data_with_overlap
import pandas as pd

# %%
class BBHash: 
    def __init__(self, keys: list):
        self.num_items = len(keys)
        self.table = BBHashTable()
        self.table.initialize(keys)

        for hashval, value in zip(keys, range(1,self.num_items+1)):
        # populate the table with the values
            self.table[hashval] = value

    def query(self, queries: list) -> list[bool]:
        
        return [self.table[key] is not None for key in queries]

# %% 
def create_hash_from_string(string: str, 
                            seed: int = 0, 
                            bitlength : int = 16
                            ) -> int:
    """
    Hash a string using Python's built-in hash() function.
    """
    return hash((string, seed)) % (2**bitlength)
    

# %%

#_, key_list, query_list, overlap = prepare_data()   

# %%

fractions = [0.5, 0.8]
final_dict  = {}


for fraction in fractions: 

    _, key_list, query_list, overlap = prepare_data_with_overlap(fraction_overlap=fraction)

    print(overlap)

    result_dict = {}

    for keys_dataset, queries_dataset in tqdm(zip(key_list, query_list)):
        keys = set(keys_dataset)
        print("keys", len(keys))
        print("queries", len(queries_dataset))

        key_hashes = [create_hash_from_string(s) for s in keys_dataset]
        query_hashes = [create_hash_from_string(s) for s in queries_dataset]
        
        temp_dict = {} 
        
        temp_dict['num_overlap'] = len(set(keys_dataset).intersection(set(queries_dataset)))
        print("num_overlap", temp_dict['num_overlap'])

        bbhashmap = BBHash(key_hashes)
        start_time = time.time()
        query_results = bbhashmap.query(query_hashes)
        end_time = time.time()
        
        bbhashmap.table.save('/tmp/bbhashmap_mph', '/tmp/bbhashmap1')
        temp_dict['filesize'] = os.path.getsize('/tmp/bbhashmap_mph')
    
        temp_dict['query_time'] = end_time - start_time
        temp_dict['false_positives'] = 0 

        unseen = 0 
        for index, query in tqdm(enumerate(queries_dataset), desc='Counting false positives') : 
            if query not in keys :
                unseen += 1
                if query_results[index]:
                    temp_dict['false_positives'] += 1

        temp_dict['fp_rate']  = temp_dict['false_positives'] / (unseen + 1)
        temp_dict['num_unseen'] = unseen 
        temp_dict['table_size'] = len(bbhashmap.table)
        temp_dict['query_size'] = len(queries_dataset)
     
        result_dict[str(len(keys_dataset))] = temp_dict

        


    df = pd.DataFrame.from_dict(result_dict)
    print(df.head(10)) 

    final_dict[str(fraction)] = df


# %%
final_dict['0.0'].head()
# %%
final_dict['0.3'].head()
# %%
final_dict['0.5'].head()
# %%
final_dict['0.8'].head()

# %%
final_dict['0.99'].head()
# %%
final_dict['1.0'].head()

# %%
import matplotlib.pyplot as plt
# %%
