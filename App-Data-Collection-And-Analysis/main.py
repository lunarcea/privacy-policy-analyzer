#####################################################################
import os, requests, json, csv, subprocess, yaml, time, re
from datetime import datetime
from dateutil.relativedelta import relativedelta
#####################################################################

# API configuration with sensitive data removed
android_api_object = {
    "api_key": "API_KEY_REMOVED",
    "app_analysis_premium": {
        "engagement":{
            "describe":{
                "url":"https://api.example.com/v4/data-ai/engagement/describe?api_key=similarweb_api_key",
                "region":"US",
                "granularity": "Monthly",
                "start_date": "2022-08",
                "end_date": "2023-10",
                "period":14
            },
            "monthly_active_users":{
                "url": "https://api.example.com/v4/data-ai/Google/app_id/mau?api_key=similarweb_api_key&start_date=user_start_date&end_date=user_end_date&country=us&granularity=monthly&device=androidPhone&format=json"
            },
            # Additional endpoints removed for brevity
        },
        # Additional categories removed for brevity
    }
}

apple_api_object = {
    "api_key": "API_KEY_REMOVED",
    "app_analysis_premium": {
        "engagement":{
            "describe":{
                "url":"https://api.example.com/v4/data-ai/engagement/describe?api_key=similarweb_api_key",
                "region":"US",
                "granularity": "Monthly",
                "start_date": "2022-04",
                "end_date": "2023-06",
                "period":14
            },
            # Additional endpoints removed for brevity
        },
        # Additional categories removed for brevity
    }
}

#####################################################################

def diff_month(end_date, start_date):
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

def get_end_month(period):
    current_month = str(datetime.now().month)
    current_year = str(datetime.now().year)
    if len(current_month) == 1:
        current_month = "0"+current_month
    end_month = datetime.strptime(str(current_year)+"-"+str(current_month), "%Y-%m")
    return end_month - relativedelta(months=2)

def get_start_month(start_month, period):
    end_date = start_month - relativedelta(months=period)
    end_month = str(end_date.month)    
    end_year = str(end_date.year)    
    if len(end_month) == 1:
        end_month = "0"+end_month
    end_date = end_year +"-"+end_month
    return end_date

def end_month_add_zero(end_month_string):
    a = end_month_string.split("-")
    b = str(a[0])
    c = str(a[1])
    if len(c) == 1:
        c = "0"+c
    return b+"-"+c

#####################################################################

def format_api_object_dates(object_item, api_response):
    object_dates = api_response["response"]["countries"][str(object_item["describe"]["region"].lower())]
    for a in object_dates:
        print("format_api_object_dates: a: ", a)
        print("format_api_object_dates: object_dates[a]: ", object_dates[a])
        print("format_api_object_dates: object_item['describe'][str(a)]: before: ", object_item["describe"][str(a)])
        object_item["describe"][str(a)] = object_dates[a]
        print("format_api_object_dates: object_item['describe'][str(a)]: after:", object_item["describe"][str(a)])
        print("format_api_object_dates: ****************************************************")
        print("format_api_object_dates: ****************************************************")

def format_api_object_describe_endpoint(api_object):
    for a in api_object:
        if type(api_object[a]) is not str:
            for b in api_object[a]:
                if type(api_object[a][b]) is not str:
                    end_date = api_object[a][b]["describe"]["end_date"] 
                    start_date = api_object[a][b]["describe"]["start_date"] 
                    for c in api_object[a][b]:
                        if type(api_object[a][b][c]) is not str and str(c) is not "describe":
                            for d in api_object[a][b][c]:
                                if d == "url":
                                    api_object[a][b][c][d] = api_object[a][b][c][d].replace("similarweb_api_key", str(api_object["api_key"])).replace("user_end_date", str(end_date)).replace("user_start_date", str(start_date))
    return api_object

#####################################################################

def open_ids_csv(filename):
    read_file = open(str(filename)+".csv","r", encoding="utf-8")
    csv_reader = csv.reader(read_file)
    return [a for a in csv_reader]
    
#####################################################################

def create_category_folder(category):
    if not os.path.exists(str(category)):
        os.makedirs(category)

#####################################################################

def gplay_app_overview(app_id):
    p = subprocess.Popen(["node", "gplay_app_overview.js", app_id], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = out.decode()
    out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
    out = re.sub(r',\s*}', r'\n}', out)
    out = re.sub(r'<[^>]*>', '', out)
    out = json.dumps(out)
    out = json.loads(out)
    out = json.dumps(yaml.load(out))
    json_format = json.loads(out)
    return json_format

def gplay_permissions(app_id):
    p = subprocess.Popen(["node", "gplay_permissions.js", app_id], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = out.decode()
    out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
    out = re.sub(r',\s*}', r'\n}', out)
    out = re.sub(r'<[^>]*>', '', out)
    out = json.dumps(out)
    out = json.loads(out)
    out = json.dumps(yaml.load(out))
    json_format = json.loads(out)
    return json_format

def gplay_developer(dev_id):
    p = subprocess.Popen(["node", "gplay_dev.js", dev_id], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = out.decode()
    out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
    out = re.sub(r',\s*}', r'\n}', out)
    out = re.sub(r'<[^>]*>', '', out)
    out = json.dumps(out)
    out = json.loads(out)
    out = json.dumps(yaml.load(out))
    json_format = json.loads(out)
    return json_format

def gplay_reviews(app_id, review_num, page_token):
    print("gplay_reviews: review_num: ", review_num)
    p = subprocess.Popen(["node", "gplay_reviews.js", app_id, "3000", page_token], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = out.decode()
    out = re.sub(r'\n\s*(\S+)\s*:', r'\n"\1":', out)
    out = re.sub(r',\s*}', r'\n}', out)
    out = re.sub(r'<[^>]*>', '', out)
    out = json.dumps(out)
    out = json.loads(out)
    out = json.dumps(yaml.load(out))
    json_format = json.loads(out)
    if json_format["nextPaginationToken"] is not page_token:
        time.sleep(0.1)
        gplay_reviews(app_id, review_num, json_format["nextPaginationToken"])
    return json_format

def gplay_data_safety(app_id):
    p = subprocess.Popen(["node", "gplay_data_safety.js", app_id], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = str(out).replace(r"\n", "")
    out = out.replace('"', '')[1:]
    out = out.replace("'", "\"")
    out = json.dumps(yaml.load(out))
    json_format = json.loads(out)
    return json_format

def gplay_all_init(app_ids):
    print("gplay_all_init: ***************** START *****************")
    current_month = str(datetime.now().month)
    if len(current_month) == 1:
        current_month = "0"+str(current_month)
    
    current_day = str(datetime.now().day)
    if len(current_day) == 1:
        current_day = "0"+str(current_day)
    
    current_year = str(datetime.now().year)
    
    for z, a in enumerate(app_ids):
        gplay_entry = {}
        print("gplay_all_init: z: ", z)
        
        save_path = str("sw_data/"+str(a[1]).lower()+"/"+a[0].replace(".", "")+"/google_play_data").replace(" ", "")
        save_filepath = str("sw_data/"+str(a[1]).lower()+"/"+a[0].replace(".", "")+"/google_play_data/"+str(a[0]).replace(".", "")+"_"+str(current_month+current_day+current_year)).replace(" ", "")
        create_category_folder(save_path)
        
        if os.path.exists(save_filepath) == False:
            app_id = a[0]
            if app_id == "com.att.callprotect":
                app_id = "com.att.mobilesecurity"
            
            print("gplay_all_init: a: ", str(a))
            print("gplay_all_init: app_id: ", str(app_id))
            app_overview = gplay_app_overview(app_id)
            print("gplay_all_init: app_overview: ", str(app_overview))
            gplay_entry["app_overview"] = app_overview
            
            dev_id = ""
            try:    
                dev_id = app_overview["developerId"]
            except:
                pass
            
            review_num = ""
            try:    
                review_num = app_overview["reviews"]
            except:
                pass
                
            time.sleep(0.1)

            dev_info = ""
            try:
                dev_info = gplay_developer(dev_id)
            except:
                pass

            gplay_entry["dev_info"] = dev_info
            time.sleep(0.1)
            
            data_safety = ""
            try:
                data_safety = gplay_data_safety(app_id)
            except:
                pass

            gplay_entry["data_safety"] = data_safety
            time.sleep(0.2)

            perm = ""
            try:
                perm = gplay_permissions(app_id)
            except:
                pass

            gplay_entry["permissions"] = perm
            time.sleep(0.1)

        if os.path.exists(save_filepath) == False:
            print("gplay_all_init: save_filepath: ", save_filepath)
            print("gplay_all_init: gplay_entry: ", gplay_entry)
            write_to_json(save_filepath, gplay_entry)

    print("gplay_all_init: ***************** END *****************")

#####################################################################

def write_to_json(filename, json_data):
    new_file = open(str(filename)+".json","w", encoding="utf-8")
    json.dump(json_data, new_file, indent=2)

def call_json_describe_endpoint(endpoint_url):
    print("call_json_describe_endpoint: endpoint_url: ", endpoint_url)
    add_key_url = endpoint_url.replace("similarweb_api_key", api_object["api_key"]) 
    print("call_json_describe_endpoint: add_key_url: ", add_key_url)
    return requests.get(add_key_url)

def call_json(endpoint_url):
    return requests.get(endpoint_url)

def format_json(json_data):
    call_get = json_data.content
    return json.loads(call_get)

#####################################################################

def android_call_api(app_ids, api_object):
    date_path_string = "sw_data_" + datetime.now().strftime("%m_%d_%Y")
    for z, a in enumerate(app_ids):
        print("android_call_api: ***************** START *****************")
        print("android_call_api: z: ", z)
        if z > 0:
            print("android_call_api: a: ", a)
            print("android_call_api: a[0]: ", a[0])
            save_path = date_path_string+"/"+a[0].replace(".", "")
            create_category_folder(save_path)
            for b in api_object:
                print("android_call_api: b: ", b)
                if type(api_object[b]) is not str:
                    for c in api_object[b]:
                        print("android_call_api: c: ", c)
                        if type(api_object[b][c]) is not str and c != "describe" and c != "affinity":
                            for d in api_object[b][c]:
                                save_filepath = date_path_string+"/"+a[0].replace(".", "")+"/"+str(a[0]).replace(".", "")+"_"+str(api_object[b][c]["describe"]["start_date"])+"_"+str(api_object[b][c]["describe"]["end_date"])+"_"+str(c)+"_"+str(d)
                                if os.path.exists(save_filepath) == False and d != "describe":
                                    print("android_call_api: d: ", d)
                                    url_add_id = api_object[b][c][d]["url"].replace("app_id", str(a[0]))
                                    print("android_call_api: url_add_id: ", url_add_id)
                                    api_response = call_json(url_add_id)
                                    print("android_call_api: api_response: ", api_response)
                                    if api_response.status_code == 200:    
                                        formatted_response = format_json(api_response)
                                        print("android_call_api: formatted_response: ", formatted_response)
                                        write_to_json(save_filepath, formatted_response)
    print("android_call_api: ***************** END *****************")

def apple_call_api(app_ids, api_object):
    for z, a in enumerate(app_ids):
        print("call_api: ***************** START *****************")
        print("call_api: z: ", z)
        if a[1] and z > 0:
            print("call_api: a: ", a)
            print("call_api: a[0]: ", a[1])
            save_path = "sw_data/"+str(a[10]).lower()+"/"+a[1].replace(".", "")
            create_category_folder(save_path)
            for b in api_object:
                print("call_api: b: ", b)
                if type(api_object[b]) is not str:
                    for c in api_object[b]:
                        print("call_api: c: ", c)
                        if type(api_object[b][c]) is not str and c != "describe" and c != "affinity":
                            for d in api_object[b][c]:
                                save_filepath = "sw_data/"+str(a[10]).lower()+"/"+a[1].replace(".", "")+"/"+str(a[0]).replace(".", "")+"_"+str(api_object[b][c]["describe"]["start_date"])+"_"+str(api_object[b][c]["describe"]["end_date"])+"_"+str(c)+"_"+str(d)
                                if os.path.exists(save_filepath) == False and d != "describe":
                                    print("call_api: d: ", d)
                                    url_add_id = api_object[b][c][d]["url"].replace("app_id", str(a[1]))
                                    print("call_api: url_add_id: ", url_add_id)
                                    api_response = call_json(url_add_id)
                                    print("call_api: api_response: ", api_response)
                                    if api_response.status_code == 200:    
                                        formatted_response = format_json(api_response)
                                        print("call_api: formatted_response: ", formatted_response)
                                        write_to_json(save_filepath, formatted_response)
    print("call_api: ***************** END *****************")

#####################################################################

def init():
    global android_api_object
    global apple_api_object
    #######################
    android_api_object = format_api_object_describe_endpoint(android_api_object)
    android_app_ids = open_ids_csv("download_list")
    android_call_api(android_app_ids, android_api_object)
    #######################

init()