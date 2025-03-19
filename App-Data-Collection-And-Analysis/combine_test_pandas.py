import pandas as pd
import os, re

# Define the directory path and output file path
dir_path = "./0_selenium_app_data"
output_path = "./test_pandas_combine_output.csv"

# Define a dictionary to store the data for each app ID and date combination
data_dict = {}

# Loop through each file in the directory
for file_name in os.listdir(dir_path):
	# Skip files that are not Excel files
	if not file_name.endswith(".xlsx"):
		continue
	
	# Get the app ID and metric from the file name
	test = ""
	app_id = file_name.replace("xlsx", "").replace(".", "")
	if "_AppsDemographics" in app_id:
		app_id = app_id.split("_AppsDemographics")[0] 
	elif "_StoreDownloads" in app_id:
		app_id = app_id.split("_StoreDownloads")[0] 
	elif "_Retention" in app_id:
		app_id = app_id.split("_Retention")[0] 
	elif "_InstallBase" in app_id:
		app_id = app_id.split("_InstallBase")[0] 
	elif "_InstallBaseDelta" in app_id:
		app_id = app_id.split("_InstallBaseDelta")[0] 
	elif "_EngagementOpenRate" in app_id:
		app_id = app_id.split("_EngagementOpenRate")[0] 
	elif "_EngagementSessions" in app_id:
		app_id = app_id.split("_EngagementSessions")[0] 

	# Load the Excel file into a dictionary of DataFrames, where each DataFrame represents a tab in the file
	file_path = os.path.join(dir_path, file_name)
	file_dict = pd.read_excel(file_path, sheet_name=None)

	# Loop through each tab in the file
	print(file_path)
	print(app_id)
	for tab_name, tab_data in file_dict.items():
		# Skip tabs that don't have any data
		if "Report Details" in str(tab_name):
			print("PASS")
			print("PASS")
			print("PASS")
			continue

		print(tab_data)
		# Get the date from the first column of the tab
		date = tab_data.iloc[0, 0]

		# Initialize a dictionary for this app ID and date combination if it doesn't exist yet
		if (app_id, date) not in data_dict:
			data_dict[(app_id, date)] = {"app_id": app_id, "Date": date}

		# Add the metric data to the dictionary
		for col_name in tab_data.columns[1:]:
			data_dict[(app_id, date)][f"{test} {col_name}"] = tab_data.loc[:, col_name].values[0]

# Convert the dictionary to a DataFrame and save it to a CSV file
data_df = pd.DataFrame(list(data_dict.values()))
print(data_df)
data_df.to_csv(output_path, index=False)