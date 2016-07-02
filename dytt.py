#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:JeffMa
# url: http://devework.com/

import os
import re
import json
import urllib2
import sys
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

reload(sys)
sys.setdefaultencoding('utf-8')


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


def get_film_info_dytt():
    items = []
    target_url = 'http://www.dy2018.com/'
    content = urllib2.urlopen(target_url).read()
    content = unicode(content,'GBK').encode('utf-8')
    only_hotl_tags = SoupStrainer(class_='co_content222')
    soup = BeautifulSoup(content, "html.parser", parse_only=only_hotl_tags)
    i = 0

    key = re.compile(r'《(.+?)》')

    for link in soup.find_all('li', limit=7):

        link_url = target_url + link.findChildren('a')[0].get('href')
        link_time = link.findChildren('span')[0].string
        link_title = link.findChildren('a')[0].get('title')[5:]

        file_name = re.findall(u'《(.*?)[【|》]', link_title)[0]

        # print file_name.encode("utf-8")

        douban_api = 'https://api.douban.com/v2/movie/search?q=' + file_name.encode("utf-8")
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(douban_api, None, headers)
        api_content = urllib2.urlopen(req)
        json_content = json.load(api_content)['subjects'][0]['images']['small']
        img_url = json_content
        #print img_url

        save_path = os.path.abspath("./icons/icon")
        img_data = urllib2.urlopen(img_url).read()
        file_name = save_path + str(i) + '.jpg'
        output = open(file_name, 'wb+')
        output.write(img_data)
        output.close()

        json_item = dict(title=link_title, subtitle='日期: '+link_time, arg=link_url, icon='icons/icon' + str(i) + '.jpg')
        items.append(json_item)
        i = i + 1

    return generate_xml(items)