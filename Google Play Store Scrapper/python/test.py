#!/usr/bin/env python3
"""
Test Script for SimilarWeb API Integration
-----------------------------------------
This script tests API endpoints and Google Play Store data retrieval.
"""

import os
import requests
import json
import csv
import subprocess
import yaml
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


# SimilarWeb API configuration
API_CONFIG = {
    "api_key": "YOUR_API_KEY_HERE",  # Replace with your actual API key
    "app_analysis_premium": {
        "engagement": {
            "describe": {
                "url": "https://api.similarweb.com/v4/data-ai/engagement/describe?api_key=similarweb_api_key",
                "region": "US",
                "granularity": "Monthly",
                "start_date": "2021-10",
                "end_date": "2022-12",
                "period": 14
            },
            "monthly_active_users": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/mau?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            }
            # Additional endpoints truncated for brevity
        }
        # Additional categories truncated for brevity
    }
}


def diff_month(end_date, start_date):
    """Calculate difference in months between two dates."""
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month


def get_end_month(period):
    """Get end month for API query based on current date minus buffer."""
    current_month = str(datetime.now().month)
    current_year = str(datetime.now().year)
    if len(current_month) == 1:
        current_month = "0" + current_month
    end_month = datetime.strptime(f"{current_year}-{current_month}", "%Y-%m")
    return end_month - relativedelta(months=2)


def get_start_month(start_month, period):
    """Calculate start month based on end month and period."""
    end_date = start_month - relativedelta(months=period)
    end_month = str(end_date.month)    
    end_year = str(end_date.year)    
    if len(end_month) == 1:
        end_month = "0" + end_month
    end_date = f"{end_year}-{end_month}"
    return end_date


def end_month_add_zero(end_month_string):
    """Ensure month has leading zero if needed."""
    parts = end_month_string.split("-")
    year = str(parts[0])
    month = str(parts[1])
    if len(month) == 1:
        month = "0" + month
    return f"{year}-{month}"


def format_api_object_dates(object_item, api_response):
    """Update API object with date information from response."""
    object_dates = api_response["response"]["countries"][object_item["describe"]["region"].lower()]
    for key in object_dates:
        print(f"Updating {key} to {object_dates[key]}")
        object_item["describe"][str(key)] = object_dates[key]


def format_api_object_describe_endpoint():
    """Prepare API object by calling describe endpoints and updating dates."""
    for category in API_CONFIG:
        if isinstance(API_CONFIG[category], dict):
            for subcategory in API_CONFIG[category]:
                if isinstance(API_CONFIG[category][subcategory], dict):
                    # Replace API key in URL
                    API_CONFIG[category][subcategory]["describe"]["url"] = API_CONFIG[category][subcategory]["describe"]["url"].replace(
                        "similarweb_api_key", str(API_CONFIG["api_key"]))
                    
                    # Call describe endpoint
                    api_response = call_json(API_CONFIG[category][subcategory]["describe"]["url"])

                    if api_response.status_code == 200:    
                        print(f"Successfully got describe data for {subcategory}")
                        formatted_response = format_json(api_response)
                        format_api_object_dates(API_CONFIG[category][subcategory], formatted_response)
                    else:
                        print(f"Failed to get describe data for {subcategory}: {api_response.status_code}")

                    # Update URLs with dates
                    end_date = API_CONFIG[category][subcategory]["describe"]["end_date"] 
                    start_date = API_CONFIG[category][subcategory]["describe"]["start_date"] 
                    
                    for endpoint in API_CONFIG[category][subcategory]:
                        if isinstance(API_CONFIG[category][subcategory][endpoint], dict) and endpoint != "describe":
                            if "url" in API_CONFIG[category][subcategory][endpoint]:
                                API_CONFIG[category][subcategory][endpoint]["url"] = API_CONFIG[category][subcategory][endpoint]["url"].replace(
                                    "similarweb_api_key", str(API_CONFIG["api_key"])).replace(
                                    "user_end_date", str(end_date)).replace(
                                    "user_start_date", str(start_date))


def open_ids_csv(filename):
    """Open CSV file and return rows."""
    with open(f"{filename}.csv", "r", encoding="utf-8") as read_file:
        csv_reader = csv.reader(read_file)
        return [a for a in csv_reader]


def create_category_folder(category):
    """Create folder if it doesn't exist."""
    if not os.path.exists(str(category)):
        os.makedirs(category)


def gplay_all_init(app_ids):
    """Test initialization of Google Play data collection."""
    for idx, app_row in enumerate(app_ids):
        if idx > 0:
            print(f"Would process app {idx}: {app_row}")


def gplay_data_safety(app_id):
    """Test retrieval of app data safety information."""
    p = subprocess.Popen(["node", "index.js", app_id], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = str(out).replace(r"\n", "")
    out = out.replace('"', '')[1:]
    out = out.replace("'", "\"")
    
    # Parse JSON
    out = json.dumps(yaml.safe_load(out))
    json_format = json.loads(out)
    
    for key in json_format:
        print(key)


def write_to_json(filename, json_data):
    """Write JSON data to file."""
    with open(f"{filename}.json", "w", encoding="utf-8") as new_file:
        json.dump(json_data, new_file, indent=2)


def call_json(endpoint_url):
    """Make HTTP request to JSON API endpoint."""
    return requests.get(endpoint_url)


def format_json(json_data):
    """Format JSON response from API."""
    call_get = json_data.content
    return json.loads(call_get)


def call_api(app_ids):
    """Test SimilarWeb API endpoints for app analytics."""
    print("Starting SimilarWeb API test...")
    
    for idx, app_row in enumerate(app_ids):
        # Skip header row
        if idx > 0:
            app_id = app_row[0]
            category = app_row[1].lower() if len(app_row) > 1 else "unknown"
            
            print(f"Would process app {idx}: {app_id} (Category: {category})")
            
            # Create directory structure for testing
            save_path = f"sw_data/{category}/{app_id.replace('.', '')}"
            create_category_folder(save_path)


def main():
    """Main function to run the test script."""
    # Prepare API configuration
    format_api_object_describe_endpoint()
    
    # Load app IDs from CSV
    app_ids = open_ids_csv("app_ids")
    print(f"Loaded {len(app_ids)} apps from CSV")
    
    # Test API calls
    call_api(app_ids)


if __name__ == "__main__":
    main()