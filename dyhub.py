#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Alfred WorkFlow DYHub
# 一个快速获取SubHD、Kat.cr、电影天堂的资源信息列表的Alfred Workflow
# author: JeffMa
# url: http://devework.com/

import sys

import alfredxml
import dytt
import katcr
import subhd

reload(sys)
sys.setdefaultencoding('utf-8')

def query(word):
    rowList=[]
    if len(word) == 0:
        rowList = [{'uid': '1',
                    'arg': '',
                    'autocomplete': '',
                    'icon': 'icon-wrong.png',
                    'subtitle': 'Optional: sub, kat, tt',
                    'title': 'Please input the variable word.'}]
        element = alfredxml.generate_xml(rowList)
        print(element)
        return
    elif word == 'sub':
        print(subhd.get_film_info_subhd())
        return
    elif word == 'kat':
        print(katcr.get_film_info_kat())
        return
    elif word == 'tt':
        print(dytt.get_film_info_dytt())
        return
    else:
        rowList = [{'uid': '1',
                    'arg': '',
                    'autocomplete': '',
                    'icon': 'icon-wrong.png',
                    'subtitle': 'Optional: sub, kat, tt',
                    'title': 'Please input the correct variable word.'}]
        element = alfredxml.generate_xml(rowList)
        print(element)
        return

# print(query('tt'))