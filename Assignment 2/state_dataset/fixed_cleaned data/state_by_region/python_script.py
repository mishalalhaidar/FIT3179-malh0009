import pandas as pd
import re

def extract_data():
    # Load datasets
    # budget_data = pd.read_csv("state-budget-2023-24-budget-website-map-data.csv")
    # budget_data = pd.read_csv("2022-23-state-budget-mapping-data.csv")
    # budget_data = pd.read_csv("2021-22-state-budget-mapping-data.csv")
    budget_data = pd.read_csv("2020-21-state-budget-mapping-data.csv")
    regions_data = pd.read_csv("state-budget.csv")

    # Clean and prepare the data for matching
    # budget_data['lga_cleaned'] = budget_data['lga'].str.strip().str.upper()
    # regions_data['LGA_cleaned'] = regions_data['LGA'].str.strip().str.upper()
    budget_data['lga_cleaned'] = budget_data['lga'].apply(lambda x: re.sub(r"\s+\(.*?\)", "", str(x)).strip().upper())
    regions_data['LGA_cleaned'] = regions_data['LGA'].str.strip().str.upper()

    # Merge the datasets on the cleaned columns
    merged_data = pd.merge(budget_data, regions_data, left_on="lga_cleaned", right_on="LGA_cleaned", how="left")

    # Remove unnecessary columns
    merged_data.drop(["LGA", "lga_cleaned", "LGA_cleaned"], axis=1, inplace=True)

    # Filter out rows where feature_type is not "LGA"
    merged_data = merged_data[merged_data["feature_type"] == "LGA"]

    # Only keep the relevant columns
    processed_data = merged_data[["Region", "lga", "investment", "type", "entity", "theme", "name", "description"]]

    # Save the processed data to a new CSV
    processed_data.to_csv("processed_state_budget.csv", index=False)

    # Check for missing regions in the merged data
    missing_regions_rows = merged_data[merged_data["Region"].isnull()]
    missing_lgas = [str(lga) for lga in missing_regions_rows["lga"].unique() if not pd.isnull(lga)]

    if missing_lgas:
        print(f"Missing regions for the following LGAs: {', '.join(missing_lgas)}")
    else:
        print("No missing regions found.")

def convert_to_numeric(value):
    try:
        if 'At least' in value:
            value = value.replace('At least', '').strip()
        # Remove dollar signs and asterisks
        value = value.replace('$', '').replace('*', '').strip()

        # Convert million to its numerical representation
        if 'million' in value:
            value = value.replace('million', '').strip()
            return float(value) * 1e6
        if 'billion' in value:
            value = value.replace('billion', '').strip()
            return float(value) * 1e9

        # For other numbers (like those in thousands), just convert to float
        return float(value)
    except:
        return value


def process_data(string):
    # Load the dataset
    df = pd.read_csv(string)

    # Drop duplicates based on the given columns
    df = df.drop_duplicates(subset=["Region", "investment", "type"])

    # Extract the specified columns
    df = df[["Region", "investment", "type", "entity", "theme", "name", "description"]]

    # Save the processed data back to the same CSV
    df.to_csv(string, index=False)

def total_tei_region():
    data = pd.read_csv("state-by-region-2020-2021.csv")
    # Group by 'Region' and sum the 'investment' column
    aggregated_data = data.groupby('Region').agg({'investment': 'sum'}).reset_index()

    # Save the resulting dataframe to a new CSV file
    aggregated_data.to_csv("total_tei_region.csv", index=False)

def add_lat_long(file):
    # Read the dataset
    data = pd.read_csv(file)

    # Group by region and sum the investment
    grouped = data.groupby('Region').agg({'investment': 'sum'}).reset_index()

    # Manually extracted coordinates for regions
    regions_coordinates = {
        "GIPPSLAND": {"longitude": 147.410, "latitude": -37.734},
        "HUME": {"longitude": 146.252, "latitude": -36.678},
        "E METRO": {"longitude": 145.612, "latitude": -37.734},
        "S METRO": {"longitude": 145.327, "latitude": -38.139},
        "N AND W METRO": {"longitude": 144.867, "latitude": -37.689},
        "LODDON MALLEE": {"longitude": 142.981, "latitude": -35.663},
        "BARWON SW": {"longitude": 142.559, "latitude": -37.997},
        "GRAMPIANS": {"longitude": 142.469, "latitude": -36.768}
    }

    # Extract the long and latitude for each region and append to dataframe
    grouped["longitude"] = grouped["Region"].apply(
        lambda x: regions_coordinates[x]["longitude"] if x in regions_coordinates else None)
    grouped["latitude"] = grouped["Region"].apply(
        lambda x: regions_coordinates[x]["latitude"] if x in regions_coordinates else None)

    # Save the dataframe to a new CSV file
    grouped.to_csv("total_tei_region.csv", index=False)


if __name__ == "__main__":
    # extract_data()
    # Read the CSV
    # df = pd.read_csv('state-by-region-2021-2022.csv')
    #
    # # Apply the conversion to the 'investment' column
    # df['investment'] = df['investment'].apply(convert_to_numeric)
    #
    # # Save the modified DataFrame back to the same CSV file
    # df.to_csv('state-by-region-2021-2022.csv', index=False)
    # print("Data has been fixed and saved!")
    strings = ["state-by-region-2020-2021.csv","state-by-region-2021-2022.csv","state-by-region-2022-2023.csv","state-by-region-2023-2024.csv"]
    #
    # for i in range(len(strings)):
    #     process_data(strings[i])
    add_lat_long(strings[3])
