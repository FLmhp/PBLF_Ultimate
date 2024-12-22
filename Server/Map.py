import pandas as pd
import requests as req
import json

AK = "e3eICqDNxNxBas5QcM3l6EBAELJNKf98"

def get_location(address):
    url = f"http://api.map.baidu.com/place/v2/search?query={address}&region=全国&output=json&ak={AK}"
    res = req.get(url)
    json_data = json.loads(res.text)

    if json_data["status"] == 0:
        lat = json_data["results"][0]["location"]["lat"]  # 纬度
        lng = json_data["results"][0]["location"]["lng"]  # 经度
    else:
        print(json_data["message"])
        return "0,0", json_data["status"]
    return str(lat) + "," + str(lng), json_data["status"]


def get_routeinfo(start, end):
    url = f"https://api.map.baidu.com/directionlite/v1/driving?origin={start}&destination={end}&ak={AK}"
    res = req.get(url)
    json_data = json.loads(res.text)

    if json_data["status"] == 0:
        return json_data["result"]["routes"][0]["distance"], json_data["result"]["routes"][0]["duration"]
    else:
        print(json_data["message"])
        return -1

def get_dist_dura(startName, endName):
    start, status1 = get_location(startName)
    end, status2 = get_location(endName)
    if status1 == 0 and status2 == 0:
        return get_routeinfo(start, end)
    else:
        return -1
    
# print(get_dist_dura("北京", "上海"))