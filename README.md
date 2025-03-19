# Privacy Policy Analyzer

A comprehensive toolkit for analyzing privacy policies and data collection practices in mobile applications, with integrated tools for data collection, processing, and analysis.

## Repository Structure

This repository contains two main branches:

1. **App-Data-Collection-and-Analysis-Toolkit**: Tools for collecting and analyzing mobile app data from multiple sources
2. **Google-Play-Store-Scraper**: Specialized tools for Google Play Store data extraction and analysis

## Overview

The Privacy Policy Analyzer project provides a suite of tools to help researchers, privacy advocates, and developers understand how mobile applications collect, process, and use personal data. By combining app store metadata with privacy policy analysis, this toolkit enables comprehensive insights into mobile app privacy practices.

## Features

### Core Features
- Privacy policy text extraction and analysis
- Detection of data collection practices
- Compliance checking against privacy regulations
- Visualization of privacy findings

### App Data Collection (App-Data-Collection-and-Analysis-Toolkit)
- Multi-platform app store metadata scraping:
  - Google Play Store (ratings, reviews, downloads, prices)
  - App Store data collection
- Historical app data through Wayback Machine archives
- SimilarWeb API integration for advanced app analytics
- Data cleaning and conversion utilities
- Automated browser interaction for data collection

### Google Play Store Scraper (Google-Play-Store-Scraper)
- App overview information retrieval
- App reviews collection and analysis
- App permissions extraction
- Developer information gathering
- Data safety information collection
- SimilarWeb API integration for extended analytics

## Prerequisites

- Python 3.6+
- Node.js (for Google Play scraping)
- Selenium WebDriver
- Chrome/Firefox browser

## Required Node.js Packages
- google-play-scraper (v9.1.1+)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/privacy-policy-analyzer.git
cd privacy-policy-analyzer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
npm install
```

4. Download and configure WebDriver for your browser:
```bash
wget https://chromedriver.storage.googleapis.com/X.XX/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/
```

5. Set up your API keys in the configuration file:
```bash
cp config.example.py config.py
# Edit config.py with your API keys
```

## Usage

### Privacy Policy Analysis
```bash
python analyze_privacy_policy.py --app-id com.example.app
```

### App Data Collection
```bash
# To access the App-Data-Collection-and-Analysis-Toolkit branch
git checkout App-Data-Collection-and-Analysis-Toolkit

# Google Play Store Data Collection
python main.py --app-id com.example.app

# Historical Data Collection
python wayback.py --app-id com.example.app

# Data Conversion
python jsontocsv.py data.json

# Excel Data Combination
python combine_xlsx.py --dir data_directory
```

### Google Play Store Scraping
```bash
# To access the Google-Play-Store-Scraper branch
git checkout Google-Play-Store-Scraper

# Retrieving App Reviews
python python/get_google_reviews.py

# Retrieving App Information
python python/gplay.py

# Using SimilarWeb Integration
python python/main.py
```

## Key Files Overview

### App-Data-Collection-and-Analysis-Toolkit Branch
- `auto_app_data_sw.py`: Automated app data collection using Selenium
- `auto_sw.py`: SimilarWeb data collection tool
- `combine_test_pandas.py`: Pandas-based data combination utility
- `combine_xlsx.py`: Excel file combination utility
- `convert_json_csv.py`: JSON to CSV conversion tool
- `fix_dates.py`: Date format normalization
- `gplay_obj.py`: Google Play data object manipulation
- `job_scraper.py`: Website job listing scraper
- `jsontocsv.py`: JSON to CSV conversion utility
- `main.py`: Main application entry point
- `wayback.py`: Wayback Machine archive retrieval tool

### Google-Play-Store-Scraper Branch
- `node/gplay_app_overview.js`: Retrieves app overview information
- `node/gplay_data_safety.js`: Retrieves app data safety information
- `node/gplay_dev.js`: Retrieves developer information
- `node/gplay_permissions.js`: Retrieves app permissions
- `node/gplay_reviews.js`: Retrieves app reviews
- `python/get_google_reviews.py`: Main script for retrieving Google Play reviews
- `python/gplay.py`: Alternative script for Google Play data
- `python/main.py`: Script with SimilarWeb API integration
- `python/test.py`: Test script

## Data Format

App IDs CSV should be formatted like this:
```
app_id,category
com.whatsapp,Social
com.instagram.android,Social
com.google.android.youtube,Entertainment
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This toolkit is for research and educational purposes only. Be sure to comply with the terms of service of any API or website you interact with, and respect all applicable privacy laws and regulations when analyzing privacy policies.
