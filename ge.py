# -*- coding: utf-8 -*-
import random
import re
from time import time,sleep,localtime
import requests
from bs4 import BeautifulSoup
import sys
import qqemail

user1 = {"no": "学号", "password": "密码"}  # 学号  # 密码

users = [user1]
data = {
    "myvs_1": "否",
    "myvs_2": "否",
    "myvs_3": "否",
    "myvs_4": "否",
    "myvs_5": "否",
    "myvs_7": "否",
    "myvs_8": "否",
    "myvs_9": "x",
    "myvs_11": "否",
    "myvs_12": "否",
    "myvs_13": "否",
    "myvs_15": "否",
    "myvs_13a": "35",
    "myvs_13b": "3501",
    "myvs_13c": "福州",
    "myvs_24": "否",
    "myvs_26": "5",
    "memo22": "成功获取",
    # 以下内容无需更改
    "did": "2",
    "door": "",
    "day6": "",
    "men6": "a",
    "sheng6": "",
    "shi6": "",
    "fun18": "220",
    "fun3": "",
    "jingdu": "139.706368",  # 经度
    "weidu": "35.687629",  # 纬度
    "ptopid": "",
    "sid": "",
}
# 以下内容无需改动
user_agent = "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"
host = "jksb.v.zzu.edu.cn"
origin = "https://jksb.v.zzu.edu.cn"
session = requests.session()
info = {}


# 登录函数
def login(account, password):
    header = {
        "Origin": origin,
        "Referer": "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0",
        "User-Agent": user_agent,
        "Host": host,
    }
    post_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login"
    post_data = {
        "uid": account,
        "upw": password,
        "smbtn": "进入健康状况上报平台",
        "hh28": "722",
    }
    response = session.post(post_url, data=post_data, headers=header)
    response.encoding = "utf-8"
    # print(response.text)
    return response.text


# 选择填报人和填报类型
def enter(html):
    url = get_url(html)
    response = session.get(url)
    response.encoding = "utf-8"
    new_html = response.text
    post_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
    refer = url + "&fun2="
    header = {
        "Origin": origin,
        "Referer": refer,
        "User-Agent": user_agent,
        "Host": host,
    }
    post_data = get_session_data(new_html)
    # print(info)
    response = session.post(post_url, data=post_data, headers=header)
    response.encoding = "utf-8"
    return response.text


# 获取选择填报人和填报类型界面的超链接
def get_url(html):
    p = re.compile(r'parent.window.location="(.*?)"')
    s = str(p.findall(html)[0]).replace("first6", "jksb")
    return s


# 获取登录的session信息
def get_session_data(html):
    keys = ["did", "door", "men6", "ptopid", "sid"]
    values = []
    soup = BeautifulSoup(html, "html.parser")
    for key in keys:
        values.append(soup.find("input", {"name": key})["value"])
    global info
    info = dict(zip(keys, values))
    return info


# 填写上报表格
def submit(data):
    url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
    refer = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb?' + data['ptopid'] + '&' + data['sid'] + '&fun2'
    headers = {
        "User-Agent": user_agent,
        "Host": host,
        "Origin": origin,
        "Referer": refer
    }
    data["ptopid"] = info.get("ptopid")
    data["sid"] = info.get("sid")
    r = requests.post(url, headers=headers, data=data)
    r.encoding = "utf-8"
    str = r.text
    t =localtime().tm_mday
    if str.find("感谢你今日上报健康状况") == -1:
        # print(str)
        qqemail.out('填报失败')
        print("填报失败",t)
    else:
        qqemail.out('填报成功')
        print(return_message(str))
        print("填报成功！",t)


def return_message(s):
    p = re.compile(r">　　(.*?)同学")
    return p.findall(s).pop()


# 三个主要功能函数聚集
def jksb(user: dict, data: dict):
    html = login(user.get("no"), user.get("password"))
    enter(html)
    submit(data)
def pi():
    console = sys.stdout                		# 得到当前输出方向， 也就是控制台
    file = open(r".\data.txt", 'w',encoding='utf-8')
    sys.stdout = file                   				# 重定向到文件
    # print('hello\n'+'java\n'+'python') 	 	# 输出到文件
    # sys.stdout = console                		# 又回到控制台
    # print(33)                           					# 在控制台打印33


# main方法
# if __name__ == "__main__":
#     # pi()
#     try:
#         for user in users:
#             jksb(user, data)
#             # sleep(random.randint(1,15))
#     except Exception as e:
#         print(e)
#     finally:
#         pass


if __name__ == "__main__":
    # pi()

    for user in users:
        jksb(user, data)
        # sleep(random.randint(1,15))
