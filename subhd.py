#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Alfred WorkFlow - SubHD.com Hot Films
# author:JeffMa
# url: http://devework.com/

import os
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


def get_film_info_subhd():
    items = []
    target_url = 'http://subhd.com'
    content = urllib2.urlopen(target_url).read().decode('utf-8')
    only_hotl_tags = SoupStrainer(class_='hotl')
    soup = BeautifulSoup(content, "html.parser", parse_only=only_hotl_tags)
    i = 0
    for link in soup.find_all('a', limit=7):
        link_url = target_url + link.get('href')
        link_img = target_url + link.findChildren('img')[0].get('src')
        cover_img = 'http://img3.doubanio.com/view/movie_poster_cover/spst/public/' + link_img.split('/sub/poster/l/')[
            1]
        link_title = link.findChildren('img')[0].get('title')

        save_path = os.path.abspath("./icons/icon")
        imgData = urllib2.urlopen(cover_img).read()
        fileName = save_path + str(i) + '.jpg'
        output = open(fileName, 'wb+')
        output.write(imgData)
        output.close()

        json_item = dict(title=link_title, subtitle='', arg=link_url, icon='icons/icon' + str(i) + '.jpg')
        items.append(json_item)
        i = i + 1

    return generate_xml(items)
