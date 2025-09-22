.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "--- Fetching METAR data ---"
	bash ./fetch_metars.sh
	@echo "--- METAR data for each airport saved as JSON files in raw_metars directory ---"


analyze: fetch
	@echo "--- Analyzing METAR data from saved JSON files in raw_metars ---"
	bash ./analyze_data.sh
	@echo "--- Analysis complete, results saved to weather_report.csv ---"


clean:
	@echo "--- Cleanup: removing raw_metars directory and weather_report.csv ---"
	rm -f weather_report.csv
	rm -rf raw_metars/
	@echo "--- Cleanup: raw_metars and weather_report.csv removed ---"
