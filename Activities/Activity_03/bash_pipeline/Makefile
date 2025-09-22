all: process_data

fetch_data:
	@echo "--- fetching data ---"
	bash ./fetch_data.sh

process_data: fetch_data
	@echo "--- processing data ---"
	bash ./process_data.sh
	@echo "--- pipeline complete ---"

clean:
	@echo "--- cleaning up ---"
	rm -f breeds.json
