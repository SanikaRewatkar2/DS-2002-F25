#!/bin/bash
set -e

# setup url and output directory
API_URL="https://api.pokemontcg.io/v2/cards"
OUTPUT_DIR="card_set_lookup" 

#https://www.copahost.com/blog/bash-commenting-3-ways-to-use-comments/ for formatting comments
#https://linuxize.com/post/bash-read/ for reading with a prompt
# prompt user
read -r -p "Enter TCG Card Set ID: " SET_ID

# catch if empty
if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

# helpful message!
echo "-> Fetching card data for $SET_ID ..."

# set up my URL and file
URL="$API_URL?q=set.id:$SET_ID"
OUTPUT_FILE="$OUTPUT_DIR/$SET_ID.json"

# curl it!
curl -s "$URL" -o "$OUTPUT_FILE" 2>&1

# catch if curl failed (based on lab 03)
if [ $? -ne 0 ]; then
    echo "Error: curl failed for $SET_ID." >&2
    exit 1
fi

# if we got nothing (invalid id) - (based on lab 03)
if [ ! -s "$OUTPUT_FILE" ] || [ "$(jq 'length' "$OUTPUT_FILE")" -eq 0 ]; then
    echo "Warning: No cards found for $SET_ID. The API returned an empty response." >&2
else # success! Helpful message for user!
    echo "-> Cards from set with ID $SET_ID saved successfully."
fi

# helpful message again!
echo "Card fetching complete!"

