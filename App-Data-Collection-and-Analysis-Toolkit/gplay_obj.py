import json, requests, ast, yaml, re, subprocess, os, time
from bs4 import BeautifulSoup as soup

# Sample structured data object (cleaned of specific identifiers)
obj_sample = {
    "key": "ds:5",
    "hash": "10",
    "data": [
        # Nested data structure with app information
        # Structure preserved but values sanitized
    ],
    "sideChannel": {}
}

def convert_to_json(string):
    # Convert string to proper JSON format
    string = string.replace("'", "\"")
    string = string.replace("\n", "")
    string = string.replace("\t", "")
    string = string.replace("\u003c", "<")
    string = string.replace("\u003e", ">")
    string = string.replace("\\\"", "\"")
    string = string.replace("null", "None")
    string = string.replace("true", "True")
    string = string.replace("false", "False")
    string = string.replace("Sideline - 2nd Line for Work Calls", "Sideline - 2nd Line for Work Calls".replace(" ", "_"))
    string = string.replace("[[", "[")
    string = string.replace("]]", "]")
    string = string.replace("[[", "[")
    string = string.replace("]]", "]")
    string = string.replace("[<", "<")
    string = string.replace(">]", ">")
    string = string.replace("<h1>", "")
    string = string.replace("</h1>", "")
    string = string.replace("<h2>", "")
    string = string.replace("</h2>", "")
    string = string.replace("<b>", "")
    string = string.replace("</b>", "")
    string = string.replace("<br>", "")
    string = string.replace("</br>", "")
    string = string.replace("<u>", "")
    string = string.replace("</u>", "")
    string = string.replace("[,", "[")
    string = string.replace(",]", "]")
    string = string.replace("'", "\"")
    json_string = json.loads(string)
    return json_string

def get_script_tag_data(url):
    response = requests.get(url)
    script_tag = ""

    if response.status_code == 200:
        page_content = response.content
        formatted = soup(response.content, 'html.parser')
        get_script = formatted.select("script")
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
                            if "+" in str(d):
                                plus_count += 1
                            
                    if plus_count >= 2:
                        return c[2]
            except:
                pass
    return None

def check_price_object(content):
    for a in content["data"]:
        for b in a:
            if "per item" in str(b).lower():
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

def extract_numbers(string):
    try:
        if isinstance(string, str):
            cleaned_string = re.sub('[^0-9]+', '', string)
            number = int(cleaned_string)
            return number
    except:
        pass
    return string

def check_price_string(content):
    if "$" in str(content):
        content = "$" + str(content.split('["$')[1].split("per item")[0]) + "per item"
        return content
    return None

def check_download_count_string(content):
    if "+" in str(content):
        content = content.split('[')
        for a in content:
            num_count = 0
            split_arr = str(a).split("]")[0].split(",")
            if "+" in str(a) and (len(split_arr) == 3 or len(split_arr) == 4) and any(c.isalpha() for c in split_arr[len(split_arr)-1]) == False:
                return extract_numbers(split_arr[len(split_arr)-1])
    return None

def init():
    # Example URL
    url = "https://web.archive.org/web/YYYYMMDDHHMMSS/https://play.google.com/store/apps/details?id=example.app.id"
    script_tag = get_script_tag_data(url)
    if isinstance(script_tag, str):
        price_check = check_price_string(script_tag)
        download_count = check_download_count_string(script_tag)
        print("price_check: string: "+str(price_check))
        print("download_count: string: "+str(download_count))
    else:
        download_count = check_download_count_object(script_tag)
        price_check = check_price_object(script_tag)
        if price_check == None:
            price_check = double_check_price_object(script_tag)
        print("price_check: object: "+str(price_check))
        print("download_count: object: "+str(download_count))

init()