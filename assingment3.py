# %% 
from utils import prepare_data, BBHash, create_hash_from_string
from importlib import reload
from tqdm.auto import tqdm
import numpy as np
import time 
import hashlib
import pandas as pd 
from utils import prepare_data_with_overlap
import os 

# %%

_, key_list, query_list, overlap = prepare_data_with_overlap(0.4)

# %%
def primary_hash(bit_length: int): 
    len_array = 2**bit_length
    return np.zeros(len_array, dtype=np.uint8)

def take_k_bits(hash_val: int, k: int) -> int:
    hash_val = hash_val >> 8
    return hash_val & ((1 << k) - 1)

# %%
#prim_hash = primary_hash(16)
# %%



df_results = {}

for f_bitsize in [8, 10, 16, 20]: 
    result_dict = {}

    for keys_dataset, queries_dataset in zip(key_list, query_list):

        keys = set(keys_dataset)
        print("keys", len(keys))
        print("queries", len(queries_dataset))

        
        key_hashes = [create_hash_from_string(s, 16) for s in keys_dataset]
        query_hashes = [create_hash_from_string(s, 16) for s in queries_dataset]
        
        #create a hash of a string using sha1

        key_sha1_hashes = [int.from_bytes(hashlib.md5(s.encode('utf-8')).digest(), byteorder='big') for s in keys_dataset]
        query_sha1_hashes = [int.from_bytes(hashlib.md5(s.encode('utf-8')).digest(), byteorder='big') for s in queries_dataset]

        # populate the fingerprint array with least significant 20 bits of the sha1 hash of keys

        fingerprint_array = primary_hash(f_bitsize)

        for hash_val in key_sha1_hashes:
            fingerprint_array[take_k_bits(hash_val, f_bitsize)] = 1

        temp_dict = {} 
        print(len(keys_dataset))
        
        temp_dict['num_overlap'] = len(set(keys_dataset).intersection(set(queries_dataset)))

        bbhashmap = BBHash(key_hashes)
        start_time = time.time()
        query_results = bbhashmap.query(query_hashes)
        end_time = time.time()
        temp_dict['query_time'] = end_time - start_time

        bbhashmap.table.save('/tmp/bbhashmap_mph', '/tmp/bbhashmap1')
        temp_dict['mphf'] = os.path.getsize('/tmp/bbhashmap_mph')
        temp_dict['total_size'] = len(fingerprint_array) * 8 + temp_dict['mphf']
        
        
        temp_dict['false_positives'] = 0 
        temp_dict['fingerprint_false_positives'] = 0

        unseen = 1

        for index, query in tqdm(enumerate(queries_dataset), desc='Counting false positives') : 
            if query not in keys :
                unseen += 1

                hashval = query_sha1_hashes[index]

                if query_results[index]:
                    temp_dict['false_positives'] += 1

                    if fingerprint_array[take_k_bits(hashval, f_bitsize)] == 1:
                        temp_dict['fingerprint_false_positives'] += 1


        temp_dict['fp_rate_with_fingerprint']  = temp_dict['fingerprint_false_positives'] / unseen
        temp_dict['fp_rate']  = temp_dict['false_positives'] / unseen
        temp_dict['query_size'] = len(queries_dataset)
        print(temp_dict['fp_rate'], temp_dict['fp_rate_with_fingerprint'], unseen)

        result_dict[str(len(keys_dataset))] = temp_dict


    df = pd.DataFrame.from_dict(result_dict)
    df = df.transpose()
    df_results[str(f_bitsize)] = df[['query_time', 'total_size', 'fp_rate', 'fp_rate_with_fingerprint', 'query_size']] 
    print(df) 

# %%
