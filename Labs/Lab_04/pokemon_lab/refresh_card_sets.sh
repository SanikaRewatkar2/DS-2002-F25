#!/bin/bash
set -e

# setup url and output directory
API_URL="https://api.pokemontcg.io/v2/cards"
DATA_DIR="card_set_lookup" 

# helpful message!
echo "Updating all current card sets in $DATA_DIR..."

# now the fun stuff (based on lab 03)
for json_file in "$DATA_DIR"/*.json; do # loop over all jsons (fun with regexes to get all ending w/ json)
    if [ -f "$json_file" ]; then # if the file exists
        # do the stuff! Update the json!
        # get the set id
        SET_ID=$(basename "$json_file" .json)
        # helpful message!
        echo "-> Updating card data for $SET_ID ..."

        # set up my URL
        URL="$API_URL?q=set.id:$SET_ID"

        # curl it!
        curl -s "$URL" -o "$json_file" 2>&1

        # catch if curl failed (based on lab 03)
        if [ $? -ne 0 ]; then
            echo "Error: curl failed for $SET_ID." >&2
            exit 1
        fi

        # if we got nothing (invalid id) - (based on lab 03)
        if [ ! -s "$json_file" ] || [ "$(jq 'length' "$json_file")" -eq 0 ]; then
            echo "Warning: No cards found for $SET_ID. The API returned an empty response." >&2
        else # success! Helpful message for user!
            echo "-> Cards from set with ID $SET_ID updated successfully."
        fi
    fi # i love how if statements end with "fi" in bash! it's so cute!
done
    
# helpful message again!
echo "Cards updated!"