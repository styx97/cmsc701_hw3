# %% Imports 
import random
from collections import defaultdict
import bbhash 
from bbhash_table import BBHashTable
from p1 import random_gen_strings
# %% 
# create data samples


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
import bbhash 
# %%
