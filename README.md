Google Play Store Scraper
A tool for scraping and analyzing app data from the Google Play Store with additional analytics integration.
Overview
This project provides scripts to scrape and analyze data from Google Play Store apps. It can retrieve:

App overview information
App reviews
App permissions
Developer information
Data safety information

It also includes optional integration with SimilarWeb API for extended app analytics.
Requirements
Python Dependencies

Python 3.6+
requests
json
csv
subprocess
yaml (ruamel.yaml)
re
time
datetime
dateutil.relativedelta

Node.js Dependencies

google-play-scraper (v9.1.1+)

Installation

Clone this repository:

Copygit clone https://github.com/yourusername/google-play-scraper.git
cd google-play-scraper

Install Python dependencies:

Copypip install requests ruamel.yaml python-dateutil

Install Node.js dependencies:

Copynpm install
Project Structure
Copygoogle-play-scraper/
├── python/
│   ├── get_google_reviews.py       # Main script for retrieving Google Play reviews
│   ├── gplay.py                    # Alternative script for Google Play data
│   ├── main.py                     # Script with SimilarWeb API integration
│   └── test.py                     # Test script
├── node/
│   ├── gplay_app_overview.js       # Retrieves app overview information
│   ├── gplay_data_safety.js        # Retrieves app data safety information
│   ├── gplay_dev.js                # Retrieves developer information
│   ├── gplay_permissions.js        # Retrieves app permissions
│   └── gplay_reviews.js            # Retrieves app reviews
├── package.json                    # Node.js package configuration
└── README.md                       # This file
Usage
Retrieving App Reviews

Create a CSV file with a list of app IDs you want to scrape (one per line)
Run the review scraper:

Copypython python/get_google_reviews.py
The script will create a directory named 0_reviews and save CSV files containing the reviews for each app.
Retrieving App Information
The gplay.py script provides functionality to get basic app information:
Copypython python/gplay.py
SimilarWeb API Integration
For extended app analytics, the main.py script provides integration with SimilarWeb API.
You'll need to provide your own API key in the script.
Copypython python/main.py
Configuration

Update the API key in main.py if you're using SimilarWeb API
Modify the input CSV file path in the respective script to point to your list of app IDs

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
License
MIT License
