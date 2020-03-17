from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import urllib.request
import time
from urllib.request import urlopen
import zipfile
import wget

import datetime as dt
from datetime import datetime
import zipfile 

import re
import seaborn as sns
import matplotlib.pyplot as plt

import statistics

from py7zr import unpack_7zarchive
import shutil

import os
from pyunpack import Archive
import zipfile

from lxml import etree
import lxml
from copy import deepcopy


def get_pairs(tup_pairs):
    if len(tup_pairs) == 0:
        return {}
    
    mut_revs = {}
    checked = []
    
    for i in tup_pairs:
        if i in checked:
            continue
        if (i[1], i[0]) in checked:
            continue
        checked.append(i)
        
        for mut_revs in tup_pairs:
            if tup_pairs == (i[1], i[0]):
                if i in mut_revs:
                    mut_revs[i] = mut_revs[i] + 1
                else:
                    mut_revs[i] = 1
                    
    return mut_revs

def get_M_perArt(revs, mut_amt, edit_num):
    if len(revs) == 0:
        return 0
    total = 0
    for i in revs:
        total = total+min(edit_num[i[0]], edit_num[i[1]])
    final = (len(mut_amt) * total)

    return final

def dicts_of_genInfo(e):
    edit_num = {}
    editor_name = {}
    
    for i in sorted(e.keys(), reverse = True):
        time = e[i][0]

        if e[i][2] != "":
            revert = int(e[i][1])
        else:
            continue
        if e[i][2] != "":
            version = int(e[i][2])
        else:
            continue
        editor = e[i][3]
        
        if editor in edit_num:
            edit_num[editor] = edit_num[editor] +1
        else:
            edit_num[editor] = 1

        if revert == 0:
            editor_name[version] = editor
    return edit_num, editor_name

def get_m_stat(e, m_val): 
    topic = e["title"]
    del e["title"]
    edit_num, editor = dicts_of_genInfo(e)
    t = []
    
    for i in sorted(e.keys(), reverse = True):
        time = e[i][0]

        if e[i][2] != "":
            revert = int(e[i][1])
        else:
            continue
        if e[i][2] != "":
            version = int(e[i][2])
        else:
            continue
        editor_name = e[i][3]

        if revert == 1:
            try:
                rival = editor[version+1]
                t.append((editor_name, rival))
            except:
                continue

    mut_pairs_amt = get_pairs(t)
    m_val = get_M_perArt(t, mut_pairs_amt, edit_num)
    
    return m_val 


def final_M_stat():
    file = open("en_light_dump.txt/en_wiki.txt", "r")
    get_each_M(file)
    
def get_each_M(file):
    m_holder = {}
    title_dict = {}
    title_dict["title"] = file.readline()
    num_edit = 0

    for i in file:
        if i[0] != "^":
            new_title = title_dict.copy()
            m_val = get_m_stat(new_title, m_holder)
            m_holder[title_dict["title"]] = m_val
            
            title_dict = {}
            title_dict["title"] = i
            edit_num = 0
        else: 
            title_dict[num_edit] = i.split(" ")
        
        num_edit = num_edit +1 
        
    new_title = title_dict.copy()
    m_val = get_m_stat(new_title, m_holder)
    m_holder[title_dict["title"]] = m_val

    
    #top 10 (can edit)
    print("Top Ten:")
    [print("topic: ",k, " m statistic: ", v) for k, v in sorted(m_holder.items(), key=lambda x: x[1], reverse=True)[:11]]
    
    #bottom 10 (can edit)
    print("\nBottom Ten:")
    [print("topic: ",k, " m value: ", v) for k, v in sorted(m_holder.items(), key=lambda x: x[1], reverse = True)[-10:]]
    
    file.close()
