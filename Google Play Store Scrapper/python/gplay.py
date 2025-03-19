#!/usr/bin/env python3
"""
Google Play Store Data Scraper
-----------------------------
This script retrieves basic app information from Google Play Store for specified app IDs.
"""

import os
import requests
import json
import csv
import subprocess
import yaml
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


def read_csv(filename):
    """Read CSV file and return rows as list."""
    with open(f"{filename}.csv", "r", encoding="utf-8", errors="ignore") as read_file:
        csv_reader = csv.reader((line.replace('\0','') for line in read_file))
        csv_rows = [a for a in csv_reader]
    return csv_rows


def open_ids_csv(filename):
    """Open CSV file and return only the first column (IDs)."""
    with open(f"{filename}.csv", "r", encoding="utf-8", errors="ignore") as read_file:
        csv_reader = csv.reader(read_file)
        return [a[0] for a in csv_reader]


def gplay_app_overview(app_id):
    """Retrieve app overview data for given app ID."""
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
    out = json.dumps(yaml.safe_load(out))
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


def gplay_reviews(app_id, review_num, page_token):
    """Recursively retrieve all reviews for an app, paginating as needed."""
    print(f"Retrieving reviews for {app_id}, page token: {page_token}")
    
    # Execute Node.js script to get reviews
    p = subprocess.Popen(["node", "gplay_reviews.js", app_id, "3000", page_token], 
                         stdout=subprocess.PIPE)
    
    out = p.stdout.read().decode()
    
    # Clean up output
    out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
    out = re.sub(r',\s*}', r'\n}', out)
    out = re.sub(r'<[^>]*>', '', out)
    
    # Parse JSON
    out = json.dumps(out)
    out = json.loads(out)
    out = json.dumps(yaml.safe_load(out))
    json_format = json.loads(out)
    
    # Write reviews to CSV
    write_object_to_csv(json_format["data"], "123.csv")
    
    # Recursively get next page of reviews if available
    if json_format["nextPaginationToken"] is not page_token:
        time.sleep(0.1)  # Rate limiting
        gplay_reviews(app_id, review_num, json_format["nextPaginationToken"])
    
    return json_format


def init_gplay(app_id_list):
    """Initialize scraping for list of app IDs."""
    for idx, app_id in enumerate(app_id_list):
        # Skip header row
        if idx > 0:
            print(f"Processing app {idx}: {app_id}")
            
            # Get app overview to determine number of reviews
            app_json = gplay_app_overview(app_id)
            num_reviews = app_json["reviews"]
            print(f"Number of reviews: {num_reviews}")
            
            # Get all reviews
            gplay_reviews(app_id, num_reviews, "")
            print("="*50)


def main():
    """Main entry point for the script."""
    filename = "appid_review_0703"
    app_id_list = open_ids_csv(filename)
    init_gplay(app_id_list)


if __name__ == "__main__":
    main()