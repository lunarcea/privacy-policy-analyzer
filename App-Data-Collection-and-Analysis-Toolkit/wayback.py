import os, sys, requests, json, csv, re, time
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout
from bs4 import BeautifulSoup as bs
from random import randint
from warnings import warn
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def read_open_csv(filename):
    a = open(filename+".csv", "r", encoding="utf-8", newline="", errors="ignore")
    b = csv.reader(a)
    c = [c for c in b]
    a.close()
    return c

def write_csv(filename):
    write_file = open(str(filename)+".csv","w", encoding="utf-8", newline="", errors="ignore")
    return [csv.writer(write_file), write_file]

def write_json_file(filename, json_content):
    print("wayback.py: write_json_file: filename: ", filename)
    a = open(filename, "w")
    json.dump(json_content, a)

def get_policy_pages(url):
    print("url: ", url)
    # Make a GET request to the URL
    add_https = "https://"+url
    if "example1" not in str(add_https) and "example2" not in str(add_https):    
        try:    
            response = requests.get(add_https)
            print("response: ", response)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page
                soup = BeautifulSoup(response.content, 'html.parser')
                # Find all the links in the page
                links = soup.find_all('a')
                # Initialize lists to store the policy URLs
                terms_and_agreements_urls = []
                privacy_policy_urls = []
                # Iterate over the links and check if they contain the keywords 'terms' or 'privacy'
                for link in links:
                    link_url = link.get('href')
                    if link_url:
                        if 'terms' in link_url.lower() or 'tos' in link_url.lower():
                            if "https://" not in str(link_url):
                                terms_and_agreements_urls.append(add_https+link_url)
                            else:
                                terms_and_agreements_urls.append(link_url)
                        elif 'privacy' in link_url.lower():
                            if "https://" not in str(link_url):
                                privacy_policy_urls.append(add_https+link_url)
                            else:
                                privacy_policy_urls.append(link_url)
                # If the policy pages were not found in the links, look for them in the sitemap
                if not terms_and_agreements_urls or not privacy_policy_urls:
                    sitemap_url = add_https + '/sitemap.xml'
                    try:
                        sitemap_response = requests.get("https://"+sitemap_url)
                        if sitemap_response.status_code == 200:
                            sitemap_soup = BeautifulSoup(sitemap_response.content, 'xml')
                            sitemap_links = sitemap_soup.find_all('loc')
                            for sitemap_link in sitemap_links:
                                sitemap_link_url = sitemap_link.text
                                if 'terms' in sitemap_link_url.lower() or 'tos' in sitemap_link_url.lower():
                                    if "https://" not in str(sitemap_link_url):
                                        terms_and_agreements_urls.append(add_https+sitemap_link_url)
                                    else:
                                        terms_and_agreements_urls.append(sitemap_link_url)
                                elif 'privacy' in sitemap_link_url.lower():
                                    if "https://" not in str(sitemap_link_url):
                                        privacy_policy_urls.append(add_https+sitemap_link_url)
                                    else:    
                                        privacy_policy_urls.append(sitemap_link_url)
                    except:
                        pass
                # Return the policy URLs
                return terms_and_agreements_urls
        except:
            pass

def get_priv(url_list):
    all_urls = []
    for a in url_list:
        links = get_policy_pages(a[0])
        if links and len(links) > 0:
            print(links)
            print("*"*50)
            print()
            all_urls.append(links)
    return all_urls

def gather_id_files():
    new_arr = []
    abc = read_open_csv("./0_archive_wayback_urls/wayback_urls_sample")
    print(abc)
    for a in abc:
        if [a[0]] not in new_arr:
            new_arr.append([a[0]])
    return new_arr

def get_ids_from_combined_file():
    url_list = read_open_csv("app_ids_sample")
    new_list = []
    for a in url_list:
        if a[0] not in new_list:
            new_list.append([a[0]])
    return new_list

def get_archives(url_list):
    print(url_list)            
    current_month = str(datetime.now().month)
    if len(current_month) == 1:
        current_month = "0"+str(current_month)
    current_day = str(datetime.now().day)
    if len(current_day) == 1:
        current_day = "0"+str(current_day)
    current_year = str(datetime.now().year)
    
    destination_dir = "0_archive_wayback_urls/"
    os.makedirs(destination_dir, exist_ok=True)

    filename = destination_dir+"wayback_google_play_archive_urls-"+current_month+"_"+current_day+"_"+current_year
    existing = []
    if os.path.exists(filename+".csv"):
        existing = read_open_csv(filename)
        csv_writer = write_csv(filename)
        write_csv_file = csv_writer[1]
        csv_writer = csv_writer[0]
        csv_writer.writerows(existing)
    else:
        csv_writer = write_csv(filename)
        write_csv_file = csv_writer[1]
        csv_writer = csv_writer[0]
        headers = ["app_id", "category", "wayback_url"]
        csv_writer.writerow(headers)

    failed_existing = []
    failed_urls_archive_path = "failed_urls_waybackpy_def_get_archives"
    if os.path.exists(failed_urls_archive_path+".csv"):
        failed_existing = read_open_csv(failed_urls_archive_path)
        failed_csv_writer = write_csv(failed_urls_archive_path)
        failed_write_csv_file = failed_csv_writer[1]
        failed_csv_writer = failed_csv_writer[0]
        failed_csv_writer.writerows(failed_existing)
    else:
        failed_csv_writer = write_csv(failed_urls_archive_path)
        failed_write_csv_file = failed_csv_writer[1]
        failed_csv_writer = failed_csv_writer[0]

    response_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        'ACCEPT' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'ACCEPT-ENCODING' : 'gzip, deflate, br',
        'ACCEPT-LANGUAGE' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'REFERER' : 'https://www.google.com/'
    }
    
    for b, a in enumerate(url_list):    
        if b > 0:
            app_id = a[0]
            app_url = "https://play.google.com/store/apps/details?id="+str(a[0])
            wayback_url = "http://web.archive.org/cdx/search/cdx?url="+str(app_url)+"&collapse=digest&from=20180101&to="+str(current_year)+str(current_month)+str(current_day)+"&output=json"
            archive_list = []
            time.sleep(0.1)
            print(app_id)
            print(app_url)
            print(wayback_url)
            try:
                response_urls = requests.get(wayback_url, headers=response_headers).text
                print(response_urls)
                parse_url = json.loads(response_urls) 

                for i in range(1,len(parse_url)):
                    orig_url = parse_url[i][2]
                    tstamp = parse_url[i][1]
                    waylink = tstamp+'/'+orig_url
                    archive_list.append("https://web.archive.org/web/"+waylink)
                for c in archive_list:
                    csv_writer.writerow([app_id, "", c])
            except:
                failed_csv_writer.writerow([app_id, wayback_url])
                pass
    write_csv_file.close()
    failed_write_csv_file.close()

def extract_numbers(string):
    try:
        if isinstance(string, str):
            cleaned_string = re.sub('[^0-9]+', '', string)
            number = int(cleaned_string)
            return number
    except:
        pass
    return string

def get_script_tag_data(content):
    script_tag = ""
    get_script = content.select("script")
    for a in get_script:
        try:    
            if "AF_initDataCallback({key: 'ds:5'" in str(a):
                script_tag = str(a).split("AF_initDataCallback(")[1].replace(");</script>", "")
                json_str = re.sub(r'([a-zA-Z_]+)\s*:', r'"\1":', script_tag)
                out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', script_tag)
                out = re.sub(r',\s*}', r'\n}', out)
                out = re.sub(r'<[^>]*>', '', out)
                out = json.dumps(out)
                out = json.loads(out)

                if "function(){return [" in str(out):
                    return str(out)

                out = json.dumps(yaml.load(out))
                script_tag = json.loads(out)
                script_tag = json.loads(json_str)
        except:
            pass    
    return script_tag

def check_download_count_object(content):
    for a in content["data"]:
        for b in a:
            try:
                for c in b:
                    plus_count = 0
                    downloads = []
                    if isinstance(c, list) and len(c) > 2:
                        for d in c:
                            print("d: ", str(d))
                            if "+" in str(d):
                                plus_count+=1
                            
                    if plus_count >= 2:
                        return c[2]
            except:
                pass
    return None

def check_price_object(content):
    for a in content["data"]:
        for b in a:
            if "per item" in str(b).lower():
                print("check_price_string: b: ", str(b))
                try:
                    for c in b:
                        if "per item" in str(c).lower():
                            return c[0]
                except:
                    pass
    return None

def double_check_price_object(content):
    for a in content["data"]:
        for b in a:
            if "$" in str(b).lower() and len(str(b)) > 50:
                try:
                    for c in b:
                        if "per item" in str(c).lower():
                            return c
                except:
                    pass
    return None

def check_price_string(content):
    if "$" in str(content):
        print("check_price_string: content: ", str(content))
        print("check_price_string: content.split([$): ", str(content.split('["$')))
        new_content = ""
        try:
            new_content = "$" + str(content.split('["$')[1].split("per item")[0]) +"per item"
        except:
            pass
        return new_content
    return None

def check_download_count_string(script_tag, content):
    num_installs = install_num_older(content)
    print("check_download_count_string: num_installs: ", str(num_installs))
    if "+" in str(script_tag):
        script_tag = script_tag.split('[')
        for a in script_tag:
            split_arr = str(a).split("]")[0].split(",")
            print(str(num_installs) in str(a))
            print(str(num_installs))
            print(str(a))
            print("*"*50)

            if str(num_installs) in str(a):
                print("check_download_count_string: a: ", str(a))
            try:
                if str(num_installs) in str(a) and len(split_arr) >= 2:
                    print("check_download_count_string: split_arr: ", str(split_arr))
                    if str(num_installs) in str(split_arr[len(split_arr)-1]) or "+" in str(split_arr[len(split_arr)-1]):
                        return extract_numbers(split_arr[len(split_arr)-2])
                    return extract_numbers(split_arr[len(split_arr)-1])
                return extract_numbers(num_installs)
            except:
                pass
    if num_installs != None and len(num_installs) > 0:
        return extract_numbers(num_installs)
    return None

def install_num_older(content):
    installs = content.select(".hAyfc")
    num_installs = None
    if len(installs) > 1:
        return str(extract_numbers(installs[2].text.replace("Installs", "")))
    elif len(installs) <= 1 or installs == None:
        installs = content.select(".ClM7O")
        if len(installs) > 1:
            return str(extract_numbers(installs[1].text.replace("Installs", "")))
    return num_installs

def string_in_array_of_arrays(str, arr):
    return any(str in subarr for subarr in arr)

def get_check_pages():
    app_ids = read_open_csv("0_archive_wayback_urls/wayback_google_play_archive_urls-sample")
    headers = ["app_id", "category", "archive_url", "archive_timestamp", "app_last_updated", "pricing", "download_estimate", "rating_score", "total_number_reviews", "5_star_reviews", "4_star_reviews", "3_star_reviews", "2_star_reviews", "1_star_reviews"]
    
    denied_headers = ["url", "status_code"]
    denied_path = "0_archive_wayback_urls/wayback_404"
    check_denied_write_csv = []
    if os.path.isfile(denied_path+".csv"):
        check_denied_write_csv = read_open_csv(denied_path) 
    else:
        check_denied_write_csv.append(denied_headers) 
    
    new_denied_csv_write = write_csv(denied_path)
    new_denied_csv_write[0].writerows(check_denied_write_csv)
    
    csv_write_path = "0_archive_wayback_urls/wayback_stats"
    check_write_csv = []
    if os.path.isfile(csv_write_path+".csv"):
        check_write_csv = read_open_csv(csv_write_path) 
    else:
        check_write_csv.append(headers)
    print("get_check_pages: os.path.isfile(csv_write_path+.csv): ", str(os.path.isfile(csv_write_path+".csv")))
    
    new_csv_write = write_csv(csv_write_path)
    new_csv_write[0].writerows(check_write_csv)
    
    response_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        "ACCEPT-ENCODING": "*",
        'REFERER' : 'https://www.google.com/',
        "CONNECTION": "keep-alive"
    }
    
    for b, a in enumerate(app_ids):
        try:
            if b > 0 and b < 500:
                if string_in_array_of_arrays(a[2], check_write_csv) == False and string_in_array_of_arrays(a[2], check_denied_write_csv) == False:
                    print("*"*50)
                    try:
                        print(a[2])
                        time.sleep(0.01)
                        response = requests.get(a[2], timeout=600, headers=response_headers)
                        print(response)
                        if response.status_code == 200:
                            contents = response.content
                            contents = soup(contents)
                            
                            archive_timestamp = get_archive_timestamp(a[2])
                            total_number_reviews = get_reviews_older_gplay(contents)
                            star_reviews = get_star_reviews_older_gplay(contents, total_number_reviews)
                            has_data_safety = False
                            
                            if star_reviews != None:
                                has_data_safety = star_reviews[1]
                                star_reviews = star_reviews[0]

                            app_last_updated = get_date_updated_older_gplay(contents)
                            rating_score = get_score_older_gplay(contents)
                            
                            price_check = None
                            download_count = None
                            installs = None
                            
                            installs = install_num_older(contents)
                            print("get_check_pages: installs: ", str(installs))

                            script_tag = get_script_tag_data(contents)
                            if script_tag != "" and isinstance(script_tag, str):
                                price_check = check_price_string(script_tag)
                                download_count = check_download_count_string(script_tag, contents)
                                print("price_check: string: "+str(price_check))
                                print("download_count: string: "+str(download_count))
                            elif script_tag != "":
                                download_count = check_download_count_object(script_tag)
                                price_check = check_price_object(script_tag)
                                if price_check == None:
                                    price_check = double_check_price_object(script_tag)
                                    print(price_check)
                                print("price_check: object: "+str(price_check))
                                print("download_count: object: "+str(download_count))
                            
                            print("price_check: final: "+str(price_check))
                            print("download_count: final: "+str(download_count))
                            
                            date_safety = []
                            if has_data_safety == True:
                                date_safety = get_data_info(contents)
                                app_last_updated = get_date_updated_newer_gplay(contents)
                                print(star_reviews)
                                
                                try:
                                    total_number_reviews = sum(star_reviews)
                                except:
                                    pass
                                
                                try:
                                    rating_score = get_score_newer_gplay(contents)
                                except:
                                    pass
                            
                            combined_arr = a+[archive_timestamp]+[app_last_updated]+[price_check]+[download_count]+[rating_score]+[total_number_reviews]+star_reviews+date_safety
                            print("combined_arr; ", str(combined_arr))
                            if combined_arr not in check_write_csv:
                                new_csv_write[0].writerow(combined_arr)
                            
                        elif response.status_code != 200:
                            print("BAD RESPONSE: ")
                            print([a[2], response.status_code])
                            new_denied_csv_write[0].writerow([a[2], response.status_code])
                            check_denied_write_csv.append([a[2], response.status_code])

                    except TimeoutError:
                        print("Connection Error")
                        new_denied_csv_write[0].writerow([a[2], "timeout"])
                        check_denied_write_csv.append([a[2], "timeout"])
                        pass
                    except ReadTimeout:
                        print("Connection Timeout")
                        new_denied_csv_write[0].writerow([a[2], "read_timeout"])
                        check_denied_write_csv.append([a[2], "read_timeout"])
                        pass
                    except:
                        print("Final Exception Pass")
                        pass
        except:
            pass

def get_archive_timestamp(url):
    url = url.split("/")
    return url[4]

def get_reviews_older_gplay(page_content):
    rating_en = page_content.select(".reviews-stats")
    rating_other = page_content.select(".EymY4b")
    rating = rating_en+rating_other
    if len(rating) > 0:
        return extract_numbers(rating[0].text) 
    return None

def get_date_updated_older_gplay(page_content):
    date_updated = page_content.select(".htlgb")
    date_updated_en = page_content.select('[itemprop="datePublished"]')
    date_updated = date_updated_en+date_updated
    if len(date_updated) > 0:
        return date_updated[0].text
    return None

def get_date_updated_newer_gplay(page_content):
    date_updated = page_content.select(".xg1aie")
    if len(date_updated) > 0:
        return date_updated[0].text
    return None

def get_score_older_gplay(page_content):
    score = page_content.select(".BHMmbe")
    score_en = page_content.select(".score")
    score = score+score_en
    if len(score) > 0:
        return score[0].text.replace(",", ".")
    return None

def get_score_newer_gplay(page_content):
    score = page_content.select(".jILTFe")
    if len(score) > 0:
        return score[0].text.replace(",", ".")
    return None

def calc_width_percent(page_content):
    star_bars = page_content.select(".mMF0fd")
    width_arr = [] 
    for a in star_bars:
        width = a.select(".L2o20d")
        width_arr.append(extract_numbers(width[0]["style"].replace("width:", "")))
    return width_arr

def substitute_width_percentage(page_content, total_number_reviews):
    star_bars = page_content.select(".mMF0fd")
    five_star = 0
    four_star = 0
    three_star = 0
    two_star = 0
    one_star = 0
    width_arr = calc_width_percent(page_content)

    try:
        five_star = extract_numbers(star_bars[0].text)
    except:
        pass
    
    try:
        four_star = extract_numbers(star_bars[1].text)
    except:
        pass
    
    try:
        three_star = extract_numbers(star_bars[2].text)
    except:
        pass
    
    try:
        two_star = extract_numbers(star_bars[3].text)
    except:
        pass
    
    try:
        one_star = extract_numbers(star_bars[4].text)
    except:
        pass            

    all_stars = [five_star, four_star, three_star, two_star, one_star]

    if [5,4,3,2,1] == all_stars:
        new_arr = []
        for b, a in enumerate(star_bars):
            new_num = a.select(".L2o20d")
            new_num_alt = a.select(".UfW5d")
            
            if len(new_num) > 0 and new_num[0].has_attr("title") == True:
                new_num = extract_numbers(new_num[0]["title"])
            elif len(new_num_alt) > 0 and new_num[0].has_attr("title") == False and new_num_alt[0].has_attr("aria-label") == True:
                new_num = a.select(".UfW5d")
                new_num = extract_numbers(new_num[0]["aria-label"])
            elif len(width_arr) > 0:
                try:
                    new_num = width_arr[b]/sum(width_arr)*total_number_reviews
                except:
                    new_num = 0
            else:
                new_num = 0
            new_arr.append(new_num)

        return new_arr

    return all_stars

def substitute_width_percentage_gplay_newer(page_content):
    new_arr = []
    
    star_bars = page_content.select(".RutFAf")
    for b, a in enumerate(star_bars):
        if a.has_attr("title") == True:
            new_arr.append(extract_numbers(a["title"]))
    return new_arr

def get_data_info(page_content):
    data_safety_list = page_content.select(".wGcURe")
    base = ["", "", "", "", ""]
    if len(data_safety_list) > 0 and "no information available" not in data_safety_list[0].text.lower():
        for a in data_safety_list:
            if "share" in str(a.text):
                base[0] = str(a.text).replace("Learn more about how developers declare sharing", "")
            elif "collect" in str(a.text):
                base[1] = str(a.text)
            elif "encrypted" in str(a.text):
                base[2] = str(a.text)
            elif "deleted" in str(a.text):
                base[3] = str(a.text)
            elif "security" in str(a.text):
                base[4] = str(a.text)
            else:
                base.append(str(a.text))

    return base

def get_star_reviews_older_gplay(page_content, total_number_reviews):
    has_data_safety = False
    
    five_star = page_content.select(".rating-bar-container.five")
    four_star = page_content.select(".rating-bar-container.four")
    three_star = page_content.select(".rating-bar-container.three")
    two_star = page_content.select(".rating-bar-container.two")
    one_star = page_content.select(".rating-bar-container.one")
    all_stars = five_star+four_star+three_star+two_star+one_star
    
    if len(all_stars) > 0:
        ratings = [extract_numbers(five_star[0].text), extract_numbers(four_star[0].text), extract_numbers(three_star[0].text), extract_numbers(two_star[0].text), extract_numbers(one_star[0].text)]
        return [ratings, has_data_safety] 
    else:
        ratings = substitute_width_percentage(page_content, total_number_reviews)
        if ratings == [0,0,0,0,0]:
            has_data_safety = True
            ratings = substitute_width_percentage_gplay_newer(page_content)
        return [ratings, has_data_safety]
    
    return None

def stats_filter_get_ids_from_combined_file(stats_file_to_filter):
    url_list = read_open_csv(stats_file_to_filter)
    new_list = []
    for a in url_list:
        if a[0] not in new_list:
            new_list.append(a[0])
    return new_list

def filter_wayback_stats(id_list, file_to_filter, output_file):
    new_csv_write = write_csv(output_file)
    stats_list = read_open_csv(file_to_filter)
    for a in stats_list:
        if a[0] in id_list:
            print(a)
            new_csv_write[0].writerow(a)

def init():
    # Option 1: Get policy pages from a list of URLs
    # url_list = read_open_csv("sample_list")
    # get_priv(url_list)
    
    # Option 2: Gather app IDs from files and get Wayback Machine archives
    # id_list = gather_id_files()
    # get_archives(id_list)
    
    # Option 3: Process information from archived pages
    # get_check_pages()
    
    # Option 4: Filter statistics based on a list of app IDs
    id_list = stats_filter_get_ids_from_combined_file("app_ids_sample")
    filter_wayback_stats(id_list, "0_archive_wayback_urls/wayback_stats_sample", "0_archive_wayback_urls/wayback_stats_filtered")

init()