# yay python time
# lets get json and pandas for this
import json
import pandas as pd # if you get the error "pandas not found waaaah", change the interpreter
import os # for directory stuffs

# load lookup dir function
def _load_lookup_dir(lookup_dir): # load json prices
    all_lookup_df = [] # here's my empty list
    # Labs\Lab_04\pokemon_lab\lookup_dir is the relative path
    # for loop over all files in lookup directory: https://pieriantraining.com/iterate-over-files-in-directory-using-python/
    for filename in os.listdir("Labs/Lab_04/pokemon_lab/{lookup_dir}".format(lookup_dir=lookup_dir)): # not efficient but i don't care
        if filename.endswith('.json'):
            filepath = "Labs/Lab_04/pokemon_lab/{lookup_dir}/{filename}".format(lookup_dir=lookup_dir, filename=filename) # construct filepath
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
    # Labs\Lab_04\pokemon_lab\inventory_dir is the relative path
    # for loop over all files in lookup directory: https://pieriantraining.com/iterate-over-files-in-directory-using-python/
    for filename in os.listdir("Labs/Lab_04/pokemon_lab/{inventory_dir}".format(inventory_dir=inventory_dir)): # not efficient but i don't care
        if filename.endswith('.csv'):
            temp_inv_df = pd.read_csv("Labs/Lab_04/pokemon_lab/{inventory_dir}/{filename}".format(inventory_dir=inventory_dir, filename=filename)) # read csv https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html#pandas.read_csv
            #print(temp_inv_df) #aaa
            inventory_data.append(temp_inv_df) # append
    print(inventory_data)
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


if __name__ == "__main__":
    #print(_load_lookup_dir("card_inventory_test"))
    print(_load_inventory_dir("card_inventory_test"))