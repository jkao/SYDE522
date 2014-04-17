import json

from trulia_cleaner import TruliaCleaner
from zillow_cleaner import ZillowCleaner

if __name__ == "__main__":
    OUTPUT_FILE = "data/cleaned.json"

    # Clean data from the two sources
    tcc = TruliaCleaner(
        "../scraper/output/trulia_properties.json",
        "data/broker_labels.json",
        "data/property_type_labels.json")
    zcc = ZillowCleaner(
        "../scraper/output/zillow_properties.json",
        "data/broker_labels.json",
        "data/property_type_labels.json")

    t_data = tcc.clean_data()
    z_data = zcc.clean_data()

    # Consolidate and normalize the data
    consolidated = t_data + z_data
    tcc.normalize_data(consolidated)

    # Output data
    with open(OUTPUT_FILE, "w") as f:
        json.dump(consolidated, f)
