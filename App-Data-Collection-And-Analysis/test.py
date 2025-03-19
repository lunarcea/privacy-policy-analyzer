#####################################################################
import os, requests, json, csv, subprocess, yaml
from datetime import datetime
from dateutil.relativedelta import relativedelta
#####################################################################

api_object = {
    "api_key": "API_KEY_REMOVED",
    "app_analysis_premium": {
        "engagement":{
            "describe":{
                "url":"https://api.example.com/v4/data-ai/engagement/describe?api_key=similarweb_api_key",
                "region":"US",
                "granularity": "Monthly",
                "start_date": "2021-10",
                "end_date": "2022-12",
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

def format_api_object_describe_endpoint():
    for a in api_object:
        if type(api_object[a]) is not str:
            for b in api_object[a]:
                if type(api_object[a][b]) is not str:
                    api_object[a][b]["describe"]["url"] = api_object[a][b]["describe"]["url"].replace("similarweb_api_key", str(api_object["api_key"]))
                    api_response = call_json(api_object[a][b]["describe"]["url"])

                    if api_response.status_code == 200:    
                        print("format_api_object: api_response.status_code: !!SUCCESS!!: ", api_response.status_code)
                        formatted_response = format_json(api_response)
                        print("format_api_object: api_object[a][b]: before: ", api_object[a][b])
                        format_api_object_dates(api_object[a][b], formatted_response)
                        print("format_api_object: api_object[a][b]: after: ", api_object[a][b])
                        print("format_api_object: ****************************************************")
                    else:
                        print("format_api_object: api_response.status_code: **FAIL**: ", api_response.status_code)

                    end_date = api_object[a][b]["describe"]["end_date"] 
                    start_date = api_object[a][b]["describe"]["start_date"] 
                    for c in api_object[a][b]:
                        if type(api_object[a][b][c]) is not str and str(c) is not "describe":
                            for d in api_object[a][b][c]:
                                if d == "url":
                                    api_object[a][b][c][d] = api_object[a][b][c][d].replace("similarweb_api_key", str(api_object["api_key"])).replace("user_end_date", str(end_date)).replace("user_start_date", str(start_date))
    print(api_object)

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

def gplay_all_init(app_ids):
    for z, a in enumerate(app_ids):
        print("gplay_all_init: ***************** START *****************")
        print("gplay_all_init: z: ", z)
        if z > 0:    
            print("gplay_all_init: a: ", a)

def gplay_data_safety(app_id):
    p = subprocess.Popen(["node", "index.js", "example.app.id"], stdout=subprocess.PIPE)
    out = p.stdout.read()
    out = str(out).replace(r"\n", "")
    out = out.replace('"', '')[1:]
    out = out.replace("'", "\"")
    print(out)
    out = json.dumps(yaml.load(out))
    json_format = json.loads(out)
    for a in json_format:
        print(a)

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

def call_api(app_ids):
    for z, a in enumerate(app_ids):
        print("call_api: ***************** START *****************")
        print("call_api: z: ", z)
        if z > 0:    
            print("call_api: a: ", a)
            print("call_api: a[0]: ", a[0])
            save_path = "sw_data/"+str(a[1]).lower()+"/"+a[0].replace(".", "")
            create_category_folder(save_path)
            for b in api_object:
                print("call_api: b: ", b)
                if type(api_object[b]) is not str:
                    for c in api_object[b]:
                        print("call_api: c: ", c)
                        if type(api_object[b][c]) is not str and c != "describe":
                            for d in api_object[b][c]:
                                save_filepath = "sw_data/"+str(a[1]).lower()+"/"+a[0].replace(".", "")+"/"+str(a[0]).replace(".", "")+"_"+str(api_object[b][c]["describe"]["start_date"])+"_"+str(api_object[b][c]["describe"]["end_date"])+"_"+str(c)+"_"+str(d)
                                if os.path.exists(save_filepath) == False and d != "describe":
                                    print("call_api: d: ", d)
                                    url_add_id = api_object[b][c][d]["url"].replace("app_id", str(a[0]))
                                    print("call_api: url_add_id: ", url_add_id)
                                    api_response = call_json(url_add_id)
                                    formatted_response = format_json(api_response)
                                    write_to_json(save_filepath, formatted_response)
    print("call_api: ***********************")

#####################################################################

def init():
    format_api_object_describe_endpoint()
    app_ids = open_ids_csv("app_ids")
    call_api(app_ids)

init()