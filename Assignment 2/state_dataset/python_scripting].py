import pandas as pd

# Load datasets
budget_data = pd.read_csv("state-budget-2023-24-budget-website-map-data.csv")
regions_data = pd.read_csv("state-budget.csv")

# Clean and prepare the data for matching
budget_data['lga_cleaned'] = budget_data['lga'].str.strip().str.upper()
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
