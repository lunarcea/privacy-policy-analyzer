# Mobile Application Data Toolkit

A comprehensive toolkit for collecting, processing, and analyzing mobile application data from various sources including Google Play Store, App Store, and SimilarWeb.

## Overview

This project provides a suite of tools to gather and analyze mobile app data, including:

- App store metadata scraping (ratings, reviews, downloads, prices)
- Historical app data through Wayback Machine archives
- SimilarWeb API integration for advanced app analytics
- Data cleaning and conversion utilities
- Automated browser interaction for data collection

## Features

### Data Collection

- Google Play Store scraping (app details, reviews, permissions, developer info)
- Wayback Machine integration to access historical app data
- SimilarWeb API client for engagement metrics
- Selenium-based automation for browser-based scraping

### Data Processing

- JSON to CSV conversion
- Data cleaning and normalization
- Excel file manipulation and combination
- Historical data comparison

### Analysis

- App installation trends
- User engagement metrics
- Demographic information
- Pricing and monetization data

## Requirements

- Python 3.6+
- Selenium WebDriver
- Chrome/Firefox browser
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/app-data-toolkit.git
   cd app-data-toolkit
   
2. Install required dependencies:
   pip install -r requirements.txt
   
3. Download and configure WebDriver for your browser:
   # Example for Chrome
    wget https://chromedriver.storage.googleapis.com/X.XX/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    chmod +x chromedriver
    mv chromedriver /usr/local/bin/

4. Set up your API keys in the configuration file:
   cp config.example.py config.py
    # Edit config.py with your API keys

## Usage
Google Play Store Data Collection
python main.py --app-id com.example.app

Historical Data Collection
# Collect historical data from Wayback Machine
python wayback.py --app-id com.example.app

Data Conversion
# Convert JSON data to CSV
python jsontocsv.py data.json

Excel Data Combination
# Combine multiple Excel files
python combine_xlsx.py --dir data_directory

## File Descriptions
- auto_app_data_sw.py: Automated app data collection using Selenium

- auto_sw.py: SimilarWeb data collection tool

- combine_test_pandas.py: Pandas-based data combination utility

- combine_xlsx.py: Excel file combination utility

- convert_json_csv.py: JSON to CSV conversion tool

- fix_dates.py: Date format normalization

- gplay_obj.py: Google Play data object manipulation

- job_scraper.py: Website job listing scraper

- jsontocsv.py: JSON to CSV conversion utility

- main.py: Main application entry point

- wayback.py: Wayback Machine archive retrieval tool

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This toolkit is for research and educational purposes only. Be sure to comply with the terms of service of any API or website you interact with.
