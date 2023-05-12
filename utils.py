# %%
import random 
from bbhash_table import BBHashTable

def random_gen_strings(str_len, total_size):
    """
    Create random strings of length between len_start and len_end
    from the space of characters A, C, T, G
    
    """
    result = set()
    
    while len(result) < total_size:
        # create a random string of length num sample_len times from the space of A, C, T, G
        result.add("".join(random.choices(['A', 'C', 'T', 'G'], k=str_len)))  

    # take a sample of size total_size from the list of strings removing duplicates
    return list(result)[:total_size]

# %%
def prepare_data():
    powers_of_two = [1/2**i for i in [7,8,10]]
    random_strings = [list(random_gen_strings(50, 1500)),
                        list(random_gen_strings(50, 15000)), 
                        list(random_gen_strings(50, 75000)),
                        list(random_gen_strings(50, 150000))]
    
    # make new sets of string that overlap with the previous sets
    key_datasets = []
    query_datasets = [] 

    overlaps = []
    sizes = [1000, 10000, 50000, 100000]
    for index, str_dataset_list in enumerate(random_strings):
        current_size = sizes[index]

        key_datasets.append(str_dataset_list[:current_size])
        query_datasets.append(str_dataset_list[current_size//2:])

        overlaps.append(len(set(query_datasets[index]).intersection(set(key_datasets[index])))) 

        print(len(key_datasets[index]), len(query_datasets[index]), overlaps[index])

    return powers_of_two, key_datasets, query_datasets, overlaps



def prepare_data_with_overlap(fraction_overlap=0.3):
    powers_of_two = [1/2**i for i in [7,8,10]]
    random_strings = [list(random_gen_strings(50, 2000)),
                        list(random_gen_strings(50, 20000)), 
                        list(random_gen_strings(50, 100000)),
                        list(random_gen_strings(50, 200000))]
    
    # make new sets of string that overlap with the previous sets
    key_datasets = []
    query_datasets = [] 

    overlaps = []
    sizes = [1000, 10000, 50000, 100000]
    for index, str_dataset_list in enumerate(random_strings):
        current_size = sizes[index]

        key_datasets.append(str_dataset_list[:current_size])
        overlapped_start_index = int(current_size * (1-fraction_overlap))

        query_datasets.append(str_dataset_list[ overlapped_start_index: overlapped_start_index + current_size])

        overlaps.append(len(set(query_datasets[index]).intersection(set(key_datasets[index])))) 

        print(len(key_datasets[index]), len(query_datasets[index]), overlaps[index])

    return powers_of_two, key_datasets, query_datasets, overlaps



# %%

# x, y, z, o = prepare_data()

# %%

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


def create_hash_from_string(string: str, 
                            seed: int = 0, 
                            bitlength : int = 16
                            ) -> int:
    """
    Hash a string using Python's built-in hash() function.
    """
    return hash((string, seed)) % (2**bitlength)