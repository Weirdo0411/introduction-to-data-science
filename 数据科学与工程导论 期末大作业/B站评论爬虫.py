import re
import requests
import json
from urllib.parse import quote
import pandas as pd
import hashlib
import urllib
import time
import csv

# 获取B站的Header
def get_Header():
    try:
        with open('bili_cookie.txt','r') as f:
            cookie=f.read().strip()
    except FileNotFoundError:
        print("[错误] 找不到 bili_cookie.txt 文件，请确认文件位置！")
        return {}
        
    header={
            "Cookie":cookie,
            "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
    }
    return header

# 通过bv号，获取视频的oid
def get_information(bv):
    try:
        resp = requests.get(f"https://www.bilibili.com/video/{bv}/?p=14&spm_id_from=pageDriver&vd_source=cd6ee6b033cd2da64359bad72619ca8a",headers=get_Header(), timeout=10)
        obj = re.compile(f'"aid":(?P<id>.*?),"bvid":"{bv}"')
        oid = obj.search(resp.text).group('id')

        obj = re.compile(r'<title data-vue-meta="true">(?P<title>.*?)</title>')
        try:
            title = obj.search(resp.text).group('title')
            title = re.sub(r'[\\/:*?"<>|]', '', title)
        except:
            title = "未识别"
    except Exception as e:
        print(f"[错误] 获取视频信息失败: {e}")
        return None, "未识别"

    return oid,title

# MD5加密
def md5(code):
    MD5 = hashlib.md5()
    MD5.update(code.encode('utf-8'))
    w_rid = MD5.hexdigest()
    return w_rid

# 轮页爬取
def start(bv, oid, pageID, count, csv_writer, is_second):
    mode = 2
    plat = 1
    type = 1  
    web_location = 1315875
    wts = int(time.time())
    
    if pageID != '':
        pagination_str = '{"offset":"%s"}' % pageID
    else:
        pagination_str = '{"offset":""}'
        
    code = f"mode={mode}&oid={oid}&pagination_str={urllib.parse.quote(pagination_str)}&plat={plat}&seek_rpid=&type={type}&web_location={web_location}&wts={wts}" + 'ea1db124af3c7062474693fa704f4ff8'
    w_rid = md5(code)
    url = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type={type}&mode={mode}&pagination_str={urllib.parse.quote(pagination_str, safe=':')}&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}"
    
    try:
        resp = requests.get(url=url, headers=get_Header(), timeout=10)
        if resp.status_code != 200:
            print(f"[警告] 请求一级评论失败，状态码: {resp.status_code}")
            return bv, oid, 0, count, csv_writer, is_second
        
        comment = json.loads(resp.content.decode('utf-8'))
        
        if 'data' not in comment:
            print(f"[警告] 响应数据异常 (可能被反爬): {comment}")
            return bv, oid, 0, count, csv_writer, is_second
            
        if comment['data']['replies'] is None:
            print("[信息] 本页无评论数据")
            return bv, oid, 0, count, csv_writer, is_second

    except Exception as e:
        print(f"[警告] 网络请求出错: {e}")
        return bv, oid, 0, count, csv_writer, is_second

    for reply in comment['data']['replies']:
        count += 1

        if count % 1000 ==0:
            print("休息一下...")
            time.sleep(5)

        try:
            parent=reply["parent"]
            rpid = reply["rpid"]
            uid = reply["mid"]
            name = reply["member"]["uname"]
            level = reply["member"]["level_info"]["current_level"]
            sex = reply["member"]["sex"]
            avatar = reply["member"]["avatar"]
            vip = "是" if reply["member"]["vip"]["vipStatus"] != 0 else "否"
            try:
                IP = reply["reply_control"]['location'][5:]
            except:
                IP = "未知"
            context = reply["content"]["message"]
            reply_time = pd.to_datetime(reply["ctime"], unit='s')
            try:
                rereply = reply["reply_control"]["sub_reply_entry_text"]
                rereply = int(re.findall(r'\d+', rereply)[0])
            except:
                rereply = 0
            like = reply['like']
            try:
                sign = reply['member']['sign']
            except:
                sign = ''
                
            csv_writer.writerow([count, parent, rpid, uid, name, level, sex, context, reply_time, rereply, like, sign, IP, vip, avatar])
            
        except Exception as e:
            continue

        if is_second and rereply !=0:
            max_sub_page = min(rereply//10+2, 6) 
            
            for page in range(1, max_sub_page):
                second_url=f"https://api.bilibili.com/x/v2/reply/reply?oid={oid}&type=1&root={rpid}&ps=10&pn={page}&web_location=333.788"
                try:
                    time.sleep(0.3)
                    sub_resp = requests.get(url=second_url, headers=get_Header(), timeout=5)
                    if sub_resp.status_code != 200: continue
                    second_comment = json.loads(sub_resp.content.decode('utf-8'))
                    if 'data' not in second_comment or second_comment['data']['replies'] is None:
                        continue
                    for second in second_comment['data']['replies']:
                        count += 1
                        try:
                            parent=second["parent"]
                            second_rpid = second["rpid"]
                            uid = second["mid"]
                            name = second["member"]["uname"]
                            level = second["member"]["level_info"]["current_level"]
                            sex = second["member"]["sex"]
                            avatar = second["member"]["avatar"]
                            vip = "是" if second["member"]["vip"]["vipStatus"] != 0 else "否"
                            try:
                                IP = second["reply_control"]['location'][5:]
                            except:
                                IP = "未知"
                            context = second["content"]["message"]
                            reply_time = pd.to_datetime(second["ctime"], unit='s')
                            like = second['like']
                            try:
                                sign = second['member']['sign']
                            except:
                                sign = ''
                            csv_writer.writerow([count, parent, second_rpid, uid, name, level, sex, context, reply_time, 0, like, sign, IP, vip, avatar])
                        except:
                            continue
                except Exception as e:
                    continue

    try:
        next_pageID = comment['data']['cursor']['pagination_reply']['next_offset']
    except:
        next_pageID = 0

    if next_pageID == 0:
        print(f"[完成] 本视频爬取完成！当前总数: {count}条。")
        return bv, oid, next_pageID, count, csv_writer, is_second
    else:
        time.sleep(0.5)
        print(f"正在爬取... 当前总数: {count}条")
        return bv, oid, next_pageID, count, csv_writer, is_second

if __name__ == "__main__":

    bv = "BV1uNk1YxEJQ"  # 换视频改这里
    TARGET_COUNT = 2000  # 爬多少条改这里

    print("[开始] 爬虫启动...")
    oid_result = get_information(bv)
    
    if oid_result[0] is None:
        print("[错误] 程序终止：无法获取视频信息")
    else:
        oid, title = oid_result
        print(f"[信息] 目标视频: {title}")
        
        next_pageID = ''
        count = 0
        is_second = True

        safe_title = title[:12] if len(title) > 0 else "bilibili_data"
        file_name = f'{safe_title}_评论.csv'

        try:
            with open(file_name, mode='w', newline='', encoding='utf-8-sig') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['序号', '上级评论ID','评论ID', '用户ID', '用户名', '用户等级', '性别', '评论内容', '评论时间', '回复数', '点赞数', '个性签名', 'IP属地', '是否是大会员', '头像'])

                while next_pageID != 0:
                    bv, oid, next_pageID, count, csv_writer, is_second = start(bv, oid, next_pageID, count, csv_writer, is_second)
                    if count >= TARGET_COUNT:
                        print(f"[结束] 已达到目标数量 {TARGET_COUNT} 条，爬虫停止！")
                        break
        except PermissionError:
            print(f"[错误] 请先关闭正在打开的 CSV 文件：{file_name}")
        except Exception as e:
            print(f"[错误] 发生未知错误: {e}")