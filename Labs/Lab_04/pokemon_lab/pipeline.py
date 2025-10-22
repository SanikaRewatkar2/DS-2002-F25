# aaaaaa almost done with the python stuff almost done!
import update_portfolio # import my step 2 file
import generate_summary # ditto for step 3 (hehe pokemon reference because ditto is also a pokemon)
# it looks like a purple blob and is very cute
import sys

def run_production_pipeline():
    print("Production Pipeline Running...", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
    print("<- Updating Card Portfolio...", file=sys.stderr) # https://pythonhow.com/how/print-to-stderr-in-python/
    update_portfolio.main()
    print("Portfolio Updated Successfully!", file=sys.stderr)
    print("<- Generating Portfolio Summary...", file=sys.stderr)
    generate_summary.main()
    print("Summary Generated Successfully!", file=sys.stderr)
    print("Production Pipeline Completed Successfully!", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
