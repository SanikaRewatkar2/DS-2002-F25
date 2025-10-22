# it's time to generate a summary!
# what's your favorite pokemon? mine is espeon :)
import json
import pandas as pd # if you get the error "pandas not found waaaah", change the interpreter
import os # for directory stuffs
import sys # for error printing
import csv # for file writing

def generate_summary(portfolio_file): 
    # check if file exists
    if not os.path.exists(portfolio_file):
        # error
        print("Error: Nonexistent Portfolio!", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
        sys.exit(1)
    # dataframe
    portfolio_df = pd.read_csv(portfolio_file)
    if portfolio_df.empty:
        print("Error: Cannot Generate Summary From Empty Portfolio!", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
        return
    # sum value
    value = portfolio_df["card_market_value"]
    total_portfolio_value = value.sum() # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html
    total_portfolio_value = round(total_portfolio_value, 2) # https://mimo.org/glossary/python/round-function
    # max value
    max_index = value.idxmax() # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.idxmax.html#pandas.DataFrame.idxmax
    max_card = portfolio_df.iloc[max_index] # https://note.nkmk.me/en/python-pandas-index-row-column/
    # print all the crap
    print("Total Portfolio Value: ${total_portfolio_value}".format(total_portfolio_value=total_portfolio_value))
    print("Most Valuable Card: ID - {card_id}, Name - {card_name}, Value - ${card_market_value}".format(card_id = max_card["card_id"], card_name=max_card["card_name"], card_market_value=max_card["card_market_value"]))


# test blocks block the test block the test
def main():
    generate_summary("./card_portfolio.csv")

def test():
    generate_summary("./test_card_portfolio.csv")

if __name__ == "__main__":
    print("Script is Starting Test Mode", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
    test()
    # now let us test main mode for a hot second
    print("Script is Starting Regular Mode", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
    main()