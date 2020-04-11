#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/4/11 17:53
# @Author  : Raymound luo
# @Mail    : luolinhao1998@gmail.com
# @File    : miaopan.py
# @Software: PyCharm
# @des     :
import requests
import json
import argparse
from contextlib import closing

TOKEN_URL = "https://api.codemao.cn/api/v2/cdn/upload/token/1"
UPLOAD_URL = "https://upload.qiniup.com/"
DOWNLOAD_URL = "https://static.codemao.cn/"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
header = {'user-agent': USER_AGENT}


def get_token():
    res = requests.get(url=TOKEN_URL, headers=header)
    res_json = res.json()
    token = res_json['data'][0]['token']
    return token


def upload(args):
    print("Upload:")
    token = get_token()
    print("Your toekn:", token)
    data = {'token': token}
    files = {'file': open(args.path, "rb")}
    res = requests.post(url=UPLOAD_URL, headers=header, data=data, files=files)
    res_json = res.json()
    print("key for download: ", res_json['key'])
    res_text = res.text
    with open("history.txt", "a") as f:
        f.write(args.path + ': ' + res_text + '\n')
    return


def download(args):
    print("Download:")
    download_url = DOWNLOAD_URL + args.key
    with closing(requests.get(download_url, headers=header, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 内容体总大小
        data_count = 0
        with open(args.path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, args.path), end=" ")
    print()
    print("Download success")
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Miaopan')
    subparsers = parser.add_subparsers(dest='method')
    subparsers.required = True
    parser_d = subparsers.add_parser('d', help='download help')
    parser_d.add_argument('-key', required=True, type=str, help='download key')
    parser_d.add_argument('-path', required=True, type=str, help='save filename')
    parser_d.set_defaults(func=download)

    parser_u = subparsers.add_parser('u', help='upload help')
    parser_u.add_argument('-path', type=str, required=True, help='upload file path')
    parser_u.set_defaults(func=upload)
    args = parser.parse_args()
    args.func(args)
