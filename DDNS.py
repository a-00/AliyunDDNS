#!/usr/bin/env python
# coding=utf-8

"""
新增域名解析记录，参数说明如下：
<accessKeyId>：填写自己的accessKey，建议使用RAM角色管理的Key
<accessSecret>：填写自己的accessSecret，建议使用RAM角色管理的Secret
"""

import os
import time
from aliyunsdkcore.client import AcsClient
from cxxh_function import wirte_to_file
from cxxh_function import add_record
from cxxh_function import update_record
from cxxh_function import Describe_Domain_Records
from cxxh_function import get_internet_ip


while True:
    # 判断存放IP的文件是否存在，不存在则创建
    if os.path.exists("./ip"):
        pass
    else:
        wirte_to_file("./ip", "0.0.0.0")

    client = AcsClient('LTAI4G3PiidWoszTkEpC9DL8', '7Dx8BPqiy0Tyq822mPDMYEKmrT7SOt', 'cn-hangzhou')

    # 通过函数获取外网ip
    ip = get_internet_ip()
    # print(ip)

    # 下面开始对比ip，如果ip与之前记录的ip一致，则不执行任何操作，如果ip有变化，则会更新本地存储文件和更新域名解析
    with open("./ip", 'r') as f:
        old_ip = f.read()
    if ip == old_ip:
        print("本地记录未更新"+"\nnew_ip:"+ip+"\nold_ip:"+old_ip)
    else:
        des_relsult = Describe_Domain_Records(client, "A", "chunxuexiahua.com")
        # 判断域名解析记录查询结果，TotalCount为0表示不存在这个域名的解析记录，需要新增一个
        if des_relsult["TotalCount"] == 0:
            add_relsult = add_record(client, "5", "600", "A", ip, "@", "chunxuexiahua.com")
            record_id = add_relsult["RecordId"]
            print("域名解析新增成功！")
            wirte_to_file("./ip", ip)
            print("本地记录已更新"+"\nnew_ip:"+ip+"\nold_ip:"+old_ip)
        # 判断域名解析记录查询结果，TotalCount为1表示存在这个域名的解析记录，需要更新解析记录，更新记录需要用到RecordId，这个在查询函数中有返回des_relsult["DomainRecords"]["Record"][0]["RecordId"]
        elif des_relsult["TotalCount"] == 1:
            record_id = des_relsult["DomainRecords"]["Record"][0]["RecordId"]
            update_record(client, "5", "600", "A", ip, "@", record_id)
            print("域名解析更新成功！")
            wirte_to_file("./ip", ip)
            print("本地记录已更新"+"\nnew_ip:"+ip+"\nold_ip:"+old_ip)
        else:
            TotalCount = des_relsult["TotalCount"]
            print("存在%d个域名解析记录值，请核查删除后再操作！" % TotalCount)
    time.sleep(120)
