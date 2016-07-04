#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Alfred WorkFlow DYHub - Kat.cr
# author:JeffMa
# url: http://devework.com/

import json
import urllib
import urllib2
import sys
import datetime
import math
from xml.etree import ElementTree as ET
from dateutil import parser

reload(sys)
sys.setdefaultencoding('utf-8')


# xxx 之前的时间转换
def timebefore(d):
    chunks = (
        (60 * 60 * 24 * 365, u'年'),
        (60 * 60 * 24 * 30, u'月'),
        (60 * 60 * 24 * 7, u'周'),
        (60 * 60 * 24, u'天'),
        (60 * 60, u'小时'),
        (60, u'分钟'),
    )
    # 如果不是datetime类型转换后与datetime比较
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    now = datetime.datetime.now()
    delta = now - d
    # 忽略毫秒
    before = delta.days * 24 * 60 * 60 + delta.seconds  # python2.7直接调用 delta.total_seconds()
    # 刚刚过去的1分钟
    if before <= 60:
        return u'刚刚'
    for seconds, unit in chunks:
        count = before // seconds
        if count != 0:
            break
    return unicode(count) + unit + u"前"


# 转换容量单位,size 为B 基本单位
def convertSize(size):
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1024)))
    p = math.pow(1024, i)
    s = round(size / p, 2)
    return '%s %s' % (s, size_name[i])


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)


def get_film_info_kat():
    items = []
    target_url = 'https://kat.cr'
    target_detail_url = 'https://kat.cr/json.php?q=category:movies'
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(target_detail_url, None, headers)
    content = urllib2.urlopen(req)
    json_content = json.load(content)
    target_content = json_content['list'][0]

    count = 1
    for item in json_content['list']:
        if count <= 10:
            item_title = item['title']
            item_link = item['link']
            pubDate = item['pubDate']
            item_pubDate = formate_time_string(pubDate)
            size = item['size']
            item_size = convertSize(size)
            item_subtitile = '发布时间: ' + item_pubDate + ' ,资源大小: ' + item_size

            json_item = dict(title=item_title, subtitle=item_subtitile, arg=item_link, icon='icon-kat.png')
            items.append(json_item)

        count = count + 1
    # print items
    return generate_xml(items)


# 转换json 中的时间段字符串为可用的时间格式
def formate_time_string(str):
    # eg.Wednesday 8 Jun 2016 18:02:30 +0000
    # 格式 %a, %d %b %Y %H:%M:%S +0000
    formate_date = parser.parse(str)  # type:datetime
    time_str = formate_date.strftime("%Y-%m-%d %H:%M:%S")
    time_rel = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")  # type:datetime
    return timebefore(time_rel)
