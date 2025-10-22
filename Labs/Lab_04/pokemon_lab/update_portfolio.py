# yay python time
# lets get json and pandas for this
import json
import pandas as pd # if you get the error "pandas not found waaaah", change the interpreter
import os # for directory stuffs
import sys # for error printing
import csv # for file writing

# load lookup dir function
def _load_lookup_dir(lookup_dir): # load json prices
    all_lookup_df = [] # here's my empty list
    # Labs\Lab_04\pokemon_lab\lookup_dir is the relative path
    # for loop over all files in lookup directory: https://pieriantraining.com/iterate-over-files-in-directory-using-python/
    for filename in os.listdir(lookup_dir): # not efficient but i don't care
        if filename.endswith('.json'):
            filepath = "./{lookup_dir}/{filename}".format(lookup_dir=lookup_dir, filename=filename) # construct filepath
            with open(filepath, "r") as f: 
                data = json.load(f) # load json
            # now time for pandas
            #print(data)
            pkmn_df = pd.json_normalize(data['data'])
            #print(pkmn_df)
            pkmn_df['card_market_value'] = pkmn_df['tcgplayer.prices.holofoil.market'] # prioritize holofoil
            # fill normal https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html and https://www.reddit.com/r/learnpython/comments/jbkwkd/how_do_i_fill_nan_values_of_a_column_with_its/
            pkmn_df['card_market_value'] = pkmn_df['card_market_value'].fillna(pkmn_df['tcgplayer.prices.normal.market'])
            # fill else with zeroes
            pkmn_df['card_market_value'] = pkmn_df['card_market_value'].fillna(0.0)
            # rename cols https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html#pandas.DataFrame.rename
            pkmn_df = pkmn_df.rename(columns={"id": "card_id", "set.id": "set_id", "set.name":"set_name"})
            # drop extraneous cols (can be commented out if this wreaks havoc on my code)
            required_cols = ["card_id", "name", "number", "set_id", "set_name", "card_market_value"]
            final_pkmn_df = pkmn_df[required_cols]
            #print(final_pkmn_df) # sanity check
            # append to df list
            all_lookup_df.append(final_pkmn_df)
    # ok time for pd.concat
    lookup_df = pd.concat(all_lookup_df)
    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first') # drop duplicates
    return lookup_df
        
# load inventory dir function
def _load_inventory_dir(inventory_dir):
    inventory_data = []
    # Labs\Lab_04\pokemon_lab\inventory_dir is the relative path (I WAS IN THE WRONG DIR)
    # for loop over all files in lookup directory: https://pieriantraining.com/iterate-over-files-in-directory-using-python/
    for filename in os.listdir(inventory_dir): # not efficient but i don't care
        if filename.endswith('.csv'):
            temp_inv_df = pd.read_csv("./{inventory_dir}/{filename}".format(inventory_dir=inventory_dir, filename=filename)) # read csv https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv
            #print(temp_inv_df) #aaa
            inventory_data.append(temp_inv_df) # append
    #print(inventory_data)
    # check if empty
    if len(inventory_data) == 0:
        return pd.DataFrame() # return empty df ( I wanted to use the "new" keyword but this isn't java aaa )
    # concat
    inventory_df = pd.concat(inventory_data)
    # construct shared keyyyyyyy
    shared_keys = []
    for index, row in inventory_df.iterrows(): # https://note.nkmk.me/en/python-pandas-dataframe-for-iteration/
        shared_keys.append("{set_id}-{card_number}".format(set_id=row["set_id"], card_number=row["card_number"]))
    # otherwise give a shared key https://note.nkmk.me/en/python-pandas-assign-append/
    inventory_df.insert(0, "card_id", shared_keys) 
    #print(inventory_df)
    return inventory_df

# now the final function
def update_portfolio(inventory_dir, lookup_dir, output_file):
    # call the other functions
    my_inventory_df = _load_inventory_dir(inventory_dir)
    my_lookup_df = _load_lookup_dir(lookup_dir)
    # check for empty inventory df https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.empty.html
    filepath = "./{output_file}".format(output_file=output_file) # construct filepath
    if my_inventory_df.empty:
        # create csv
        headers = ["index", "card_id", "card_name", "card_number", "set_id", "set_name", "binder_name", "page_number", "slot_number", "card_market_value"]
        with open(filepath, "w", newline='') as f: # https://www.pythontutorial.net/python-basics/python-write-csv-file/
            writer = csv.writer(f)
            writer.writerow(headers)
        print("Error: Empty Inventory!", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
        return
    # otherwise, full steam ahead
    #print(my_inventory_df)
    #print(my_lookup_df)
    final_inventory_df = my_inventory_df.merge(my_lookup_df, how='left', on='card_id') # https://pandas.pydata.org/docs/reference/api/pandas.merge.html
    # now I need to do even more cleanup
    final_inventory_df = final_inventory_df.rename(columns={"set_id_x": "set_id"})
    final_cols = ["card_id", "card_name", "card_number", "set_id", "set_name", "binder_name", "page_number", "slot_number", "card_market_value"] # final cols v1
    final_inventory_df = final_inventory_df[final_cols]
    # moar cleanup
    # fill NaN market value with zeroes
    final_inventory_df['card_market_value'] = final_inventory_df['card_market_value'].fillna(0.0)
    # fill NaN set names with "NOT FOUND"
    final_inventory_df['set_name'] = final_inventory_df['set_name'].fillna("NOT_FOUND")
    # make index
    # construct shared keyyyyyyy
    indices = []
    for index, row in final_inventory_df.iterrows(): # https://note.nkmk.me/en/python-pandas-dataframe-for-iteration/
        indices.append("{binder_name}{page_number}{slot_number}".format(binder_name=row["binder_name"], page_number=row["page_number"], slot_number=row["slot_number"]))
    # otherwise give a shared key https://note.nkmk.me/en/python-pandas-assign-append/
    final_inventory_df.insert(0, "index", indices) 
    #print(final_inventory_df) # SANIRY CHECK
    final_cols.insert(0, "index")
    # now csv mcgee stuff
    final_inventory_df.to_csv(filepath, index=False) # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
    print("Card Portfolio Successfully Updated!")

# ok time for main and test
def main():
    update_portfolio("./card_inventory", "./card_set_lookup", "card_portfolio.csv") # i set my filepaths up wrong but who cares :)

def test():
    update_portfolio("./card_inventory_test", "./card_set_lookup_test", "test_card_portfolio.csv") # i set my filepaths up wrong but who cares :)

if __name__ == "__main__":
    #print(_load_lookup_dir("card_set_lookup_test"))
    #print(_load_inventory_dir("card_inventory_test"))
    print("Script is Starting Test Mode", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
    test()
    # now let us test main mode for a hot second
    #print("Script is Starting Regular Mode", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
    #main()