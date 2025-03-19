#!/usr/bin/env python3
"""
Google Play Store Scraper with SimilarWeb API Integration
--------------------------------------------------------
This script retrieves data from Google Play Store and integrates with SimilarWeb API
for extended app analytics.
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
            },
            "install_base": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/install-base?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            "total_time": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/total-time?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            "total_sessions": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/total-sessions?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            "average_monthly_user_sessions": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/average-monthly-user-sessions?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            "average_monthly_user_time_spent": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/average-monthly-user-time-spent?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            "average_session_length": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/average-session-length?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            "open_rate": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/open-rate?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            }
        },
        "retention": {
            "describe": {
                "url": "https://api.similarweb.com/v4/data-ai/retention-d30/describe?api_key=similarweb_api_key",
                "region": "US",
                "granularity": "Monthly",
                "start_date": "2020-10",
                "end_date": "2022-11",
                "period": 24
            },
            "day_30_retention": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/retention-d30?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            }
        },
        "affinity": {
            "describe": {
                "url": "https://api.similarweb.com/v4/data-ai/audience-interests/describe?api_key=similarweb_api_key",
                "region": "US",
                "granularity": "Monthly",
                "start_date": "2021-10",
                "end_date": "2022-12",
                "period": 14
            },
            "affinity": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/audience-interests?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json&limit=100"
            }
        },
        "downloads": {
            "describe": {
                "url": "https://api.similarweb.com/v4/data-ai/engagement/downloads/describe?api_key=similarweb_api_key",
                "region": "World",
                "granularity": "Monthly",
                "start_date": "2021-10",
                "end_date": "2022-12",
                "period": 14
            },
            "downloads": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/downloads?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=world&granularity=monthly&format=json"
            }
        },
        "audience": {
            "describe": {
                "url": "https://api.similarweb.com/v4/data-ai/demographics/describe?api_key=similarweb_api_key",
                "region": "US",
                "granularity": "Monthly",
                "start_date": "2021-10",
                "end_date": "2022-12",
                "period": 14
            },
            "app_demographics_age": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/demographics/age?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&format=json"
            },
            "app_demographics_gender": {
                "url": "https://api.similarweb.com/v4/data-ai/Google/app_id/demographics/gender?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&format=json"
            }
        },
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


def gplay_app_overview(app_id):
    """Retrieve app overview data from Google Play Store."""
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


def gplay_permissions(app_id):
    """Retrieve app permissions data from Google Play Store."""
    p = subprocess.Popen(["node", "gplay_permissions.js", app_id], stdout=subprocess.PIPE)
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


def gplay_developer(dev_id):
    """Retrieve developer data from Google Play Store."""
    p = subprocess.Popen(["node", "gplay_dev.js", dev_id], stdout=subprocess.PIPE)
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


def gplay_reviews(app_id, review_num, page_token):
    """Retrieve app reviews from Google Play Store."""
    print(f"Retrieving reviews for {app_id}, page token: {page_token}")
    
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
    
    # Recursively get next page of reviews if available
    if json_format["nextPaginationToken"] is not page_token:
        time.sleep(0.1)  # Rate limiting
        gplay_reviews(app_id, review_num, json_format["nextPaginationToken"])
    
    return json_format


def gplay_data_safety(app_id):
    """Retrieve app data safety information from Google Play Store."""
    p = subprocess.Popen(["node", "gplay_data_safety.js", app_id], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = str(out).replace(r"\n", "")
    out = out.replace('"', '')[1:]
    out = out.replace("'", "\"")
    
    # Parse JSON
    out = json.dumps(yaml.safe_load(out))
    json_format = json.loads(out)
    
    return json_format


def gplay_all_init(app_ids):
    """Initialize Google Play data collection for all app IDs."""
    print("Starting Google Play data collection...")
    
    # Get current date components for filenames
    current_month = str(datetime.now().month)
    if len(current_month) == 1:
        current_month = "0" + str(current_month)
    
    current_day = str(datetime.now().day)
    if len(current_day) == 1:
        current_day = "0" + str(current_day)
    
    current_year = str(datetime.now().year)
    
    # Process each app
    for idx, app_row in enumerate(app_ids):
        
        # Skip header row
        if idx > 0:
            app_id = app_row[0]
            category = app_row[1].lower() if len(app_row) > 1 else "unknown"
            
            print(f"Processing app {idx}: {app_id} (Category: {category})")
            
            # Handle special case for certain app IDs
            if app_id == "com.att.callprotect":
                app_id = "com.att.mobilesecurity"
            
            # Create directory structure
            save_path = f"sw_data/{category}/{app_id.replace('.', '')}/google_play_data"
            save_filepath = f"{save_path}/{app_id.replace('.', '')}_{current_month}{current_day}{current_year}"
            create_category_folder(save_path)
            
            # Check if data already exists
            if not os.path.exists(save_filepath):
                gplay_entry = {}
                
                # Get app overview data
                app_overview = gplay_app_overview(app_id)
                gplay_entry["app_overview"] = app_overview
                dev_id = app_overview["developerId"]
                review_num = app_overview["reviews"]
                time.sleep(0.1)
                
                # Get developer information
                dev_info = gplay_developer(dev_id)
                gplay_entry["dev_info"] = dev_info
                time.sleep(0.1)
                
                # Get data safety information
                data_safety = gplay_data_safety(app_id)
                gplay_entry["data_safety"] = data_safety
                time.sleep(0.2)
                
                # Get permission information
                perm = gplay_permissions(app_id)
                gplay_entry["permissions"] = perm
                time.sleep(0.1)
                
                # Save all data to JSON file
                print(f"Saving data to {save_filepath}")
                write_to_json(save_filepath, gplay_entry)
            else:
                print(f"Data for {app_id} already exists at {save_filepath}")
                
    print("Google Play data collection completed.")


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
    """Call SimilarWeb API endpoints for app analytics."""
    print("Starting SimilarWeb API data collection...")
    
    for idx, app_row in enumerate(app_ids):
        # Skip header row
        if idx > 0:
            app_id = app_row[0]
            category = app_row[1].lower() if len(app_row) > 1 else "unknown"
            
            print(f"Processing app {idx}: {app_id} (Category: {category})")
            
            # Create directory structure
            save_path = f"sw_data/{category}/{app_id.replace('.', '')}"
            create_category_folder(save_path)
            
            # Process API categories
            for category_key in API_CONFIG:
                if isinstance(API_CONFIG[category_key], dict):
                    for subcategory in API_CONFIG[category_key]:
                        if isinstance(API_CONFIG[category_key][subcategory], dict):
                            
                            # Process endpoints
                            for endpoint in API_CONFIG[category_key][subcategory]:
                                if isinstance(API_CONFIG[category_key][subcategory][endpoint], dict) and endpoint != "describe":
                                    # Create file path for saving data
                                    start_date = API_CONFIG[category_key][subcategory]["describe"]["start_date"]
                                    end_date = API_CONFIG[category_key][subcategory]["describe"]["end_date"]
                                    save_filepath = f"{save_path}/{app_id.replace('.', '')}_{start_date}_{end_date}_{subcategory}_{endpoint}"
                                    
                                    # Check if data already exists
                                    if not os.path.exists(save_filepath):
                                        # Replace app_id in URL
                                        url = API_CONFIG[category_key][subcategory][endpoint]["url"].replace("app_id", app_id)
                                        print(f"Calling API: {url}")
                                        
                                        # Make API request
                                        api_response = call_json(url)
                                        
                                        if api_response.status_code == 200:
                                            # Format and save response
                                            formatted_response = format_json(api_response)
                                            write_to_json(save_filepath, formatted_response)
                                            print(f"Successfully saved data to {save_filepath}")
                                        else:
                                            print(f"API call failed: {api_response.status_code}")
                                    else:
                                        print(f"Data already exists at {save_filepath}")
    
    print("SimilarWeb API data collection completed.")


def main():
    """Main function to run the script."""
    # Prepare API configuration
    format_api_object_describe_endpoint()
    
    # Load app IDs from CSV
    app_ids = open_ids_csv("add_ids_03")
    print(f"Loaded {len(app_ids)} apps from CSV")
    
    # Call SimilarWeb API for app analytics
    call_api(app_ids)
    
    # Get Google Play data
    gplay_all_init(app_ids)


if __name__ == "__main__":
    main()