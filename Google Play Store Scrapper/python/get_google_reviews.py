#!/usr/bin/env python3
"""
Google Play Store Review Scraper
--------------------------------
This script retrieves and saves reviews from Google Play Store for specified app IDs.
"""

import os
import json
import csv
import subprocess
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from ruamel.yaml import YAML


def read_csv(filename):
    """Read CSV file and return rows as list."""
    with open(str(filename), "r", encoding="utf-8", errors="ignore") as read_file:
        csv_reader = csv.reader((line.replace('\0', '') for line in read_file))
        csv_rows = [a for a in csv_reader]
    return csv_rows


def open_ids_csv(filename):
    """Open CSV file and return only the first column (IDs)."""
    with open(f"{filename}.csv", "r", encoding="utf-8", errors="ignore") as read_file:
        csv_reader = csv.reader(read_file)
        return [a[0] for a in csv_reader]


def open_csv(filename):
    """Open CSV file and return all rows."""
    with open(f"{filename}.csv", "r", encoding="utf-8", errors="ignore") as read_file:
        csv_reader = csv.reader(read_file)
        return [a for a in csv_reader]


def write_csv(filename, data):
    """Write data to CSV file."""
    with open(f"{filename}.csv", 'w', newline='', encoding='utf-8', errors='ignore') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def strip_invalid(s):
    """Remove non-printable characters from string."""
    from ruamel.yaml.reader import Reader
    res = ''
    for x in s:
        if Reader.NON_PRINTABLE.match(x):
            continue
        res += x
    return res


def gplay_app_overview(app_id):
    """Retrieve app overview data for given app ID."""
    yaml = YAML(typ='safe')
    
    # Execute Node.js script to get app overview
    p = subprocess.Popen(["node", "gplay_app_overview.js", app_id], stdout=subprocess.PIPE)
    out = p.stdout.read().decode()
    
    # Clean up output
    out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
    out = re.sub(r',\s*}', r'\n}', out)
    out = re.sub(r'<[^>]*>', '', out)
    
    # Parse JSON
    out = json.dumps(out)
    out = json.loads(out)
    out = json.dumps(yaml.load(strip_invalid(out)))
    json_format = json.loads(out)
    
    return json_format


def write_object_to_csv(reviews_array, filename):
    """Write reviews to CSV file with criteria values as columns."""
    for obj in reviews_array:
        # Get all unique criteria values
        criteria_values = set()
        for criteria in obj.get('criterias', []):
            criteria_values.add(criteria['criteria'])

        # Create a list of fieldnames for CSV header
        fieldnames = list(obj.keys()) + list(criteria_values)

        # Write object to CSV file
        with open(filename, 'a', newline='', encoding='utf-8', errors='ignore') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            
            # Create row with criteria values mapped to columns
            row_data = {**obj}
            for criteria in criteria_values:
                row_data[criteria] = next((c['rating'] for c in obj['criterias'] 
                                          if c['criteria'] == criteria), None)
            
            writer.writerow(row_data)


def gplay_reviews(app_id, review_num, page_token, row_is_dupe=False):
    """Recursively retrieve all reviews for an app, paginating as needed."""
    yaml = YAML(typ='safe')
    
    print(f"Retrieving reviews for {app_id}, page token: {page_token}")
    
    if page_token is not None:
        # Execute Node.js script to get reviews
        p = subprocess.Popen(["node", "gplay_reviews.js", app_id, str(review_num), page_token], 
                             stdout=subprocess.PIPE)
        
        out = p.stdout.read().decode()
        
        # Clean up output
        out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
        out = re.sub(r',\s*}', r'\n}', out)
        out = re.sub(r'<[^>]*>', '', out)
        
        # Parse JSON
        out = json.dumps(out)
        out = json.loads(out)
        
        try:
            out = json.dumps(yaml.load(strip_invalid(out)))
            json_format = json.loads(out)
            
            # Prepare file path for saving reviews
            filename = app_id.replace(".", "_")
            file_path = f"./0_reviews/{filename}.csv"
            
            # Check for existing reviews if row_is_dupe is True
            existing_rows = []
            if os.path.exists(file_path) and row_is_dupe:
                try:
                    existing_rows = read_csv(file_path)
                except IOError:
                    print(f"An error occurred while reading the file '{file_path}'.")
            
            # Write reviews to CSV if not duplicates
            if json_format["data"][0] not in existing_rows:
                print(f"New review found: {json_format['data'][0]}")
                write_object_to_csv(json_format["data"], file_path)
                row_is_dupe = False
            
            # Recursively get next page of reviews if available
            if json_format["nextPaginationToken"] is not page_token:
                time.sleep(0.1)  # Rate limiting
                gplay_reviews(app_id, review_num, json_format["nextPaginationToken"], row_is_dupe)
            
            return json_format
        
        except Exception as e:
            print(f"Error processing reviews for {app_id}: {str(e)}")


def init_gplay(app_id_list):
    """Initialize review scraping for list of app IDs."""
    # Ensure output directory exists
    os.makedirs("0_reviews", exist_ok=True)
    
    # Process each app ID
    for a, app_id in enumerate(app_id_list):
        # Skip header row
        if a > 0:
            print(f"Processing app {a}: {app_id}")
            
            # Handle special cases for certain app IDs
            if app_id == "com.att.callprotect":
                app_id = "com.att.mobilesecurity"
            elif app_id == "jp.pxv.android":
                app_id = "jp.pxv.android.manga"
            
            # Get app overview to determine number of reviews
            app_json = gplay_app_overview(app_id)
            if app_json:
                num_reviews = app_json["reviews"]
                print(f"Number of reviews: {num_reviews}")
                
                # Get all reviews
                gplay_reviews(app_id, num_reviews, "", True)
                print("="*50)


def scan_dupes(app_id_list):
    """Remove duplicate app IDs from list."""
    new_id_list = []
    new_csv_array = []
    
    for row in app_id_list:
        if row[0] not in new_id_list:
            new_id_list.append(row[0])
            new_csv_array.append(row)
    
    return [new_id_list, new_csv_array]


def scan_not_downloaded(app_id_list, download_dir):
    """Find app IDs not yet downloaded."""
    not_downloaded = []
    download_list = [a.replace(".csv", "").replace("_", ".") 
                    for a in os.listdir(download_dir)]
    
    for idx, app_id in enumerate(app_id_list):
        if idx > 0 and app_id not in download_list:
            not_downloaded.append(app_id)
    
    return not_downloaded


def main():
    """Main entry point for the script."""
    app_id_filename = "list_review_download_rest_100323"
    app_id_list = open_ids_csv(app_id_filename)
    
    print(f"Loaded {len(app_id_list)} app IDs from {app_id_filename}.csv")
    print(f"First app ID: {app_id_list[0]}")
    
    init_gplay(app_id_list)


if __name__ == "__main__":
    main()