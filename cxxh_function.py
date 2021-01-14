from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
import urllib.request
import json


# 写入文件
def wirte_to_file(path, content):
    with open(path, 'w') as f:
        f_name = open(path, 'w')
        f_name.write(content)


# 新增解析记录，返回json格式的数据
def add_record(client, priority, ttl, record_type, value, rr, domainname):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')

    request.set_Priority(priority)
    request.set_TTL(ttl)
    request.set_Value(value)
    request.set_Type(record_type)
    request.set_RR(rr)
    request.set_DomainName(domainname)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult


# 更新解析记录
def update_record(client, priority, ttl, record_type, value, rr, record_id):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_Priority(priority)
    request.set_TTL(ttl)
    request.set_Value(value)
    request.set_Type(record_type)
    request.set_RR(rr)
    request.set_RecordId(record_id)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    return response


# 获取解析记录列表
def Describe_Domain_Records(client, record_type, domainname):
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_Type(record_type)
    request.set_DomainName(domainname)

    response = client.do_action_with_exception(request)
    response = str(response, encoding='utf-8')
    relsult = json.loads(response)
    return relsult


# 获取外网地址
def get_internet_ip():
    with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
        html = response.read()
        ip = str(html, encoding='utf-8').replace("\n", "")
    return ip


# 测试地址
# def get_internet_ip():
#     ip = '27.191.201.216'
#     return ip
