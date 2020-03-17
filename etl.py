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

#download raw data
def download_raw():
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

    url = 'https://dumps.wikimedia.org/enwiki/20200101/'
    url2 = 'https://dumps.wikimedia.org/'
    opened = urlopen(url)

    soup = BeautifulSoup(opened, 'lxml')
    all_links = soup.findAll('a')

    first_tag = soup.findAll('a')[127]
    second_tag = soup.findAll('a')[128]

    link_first = first_tag['href']
    link_second = second_tag['href']

    link1 = first_tag.get("href")
    link2 = second_tag.get("href")

    link1 = first_tag.get("href")
    link2 = second_tag.get("href")

    wget.download(first_file, "file1.7z")
    wget.download(second_file, "file2.7z")

def unzip_raw():
    shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
    shutil.unpack_archive('./file1.7z')
    shutil.unpack_archive('./file2.7z')

def fast_iter(context):
    '''loops through an XML object, and writes 1000 page elements per file.'''
    page_num = 1
    
    # create an empty tree to add XML elements to ('pages')
    # and a new file to write to.
    fh = make_tmpfile(page_num)
    tree = etree.ElementTree()
    root = etree.Element("wikimedia")
    
    # loop through the large XML tree (streaming)
    for event, elem in context:
        print(page_num)
        # After 1000 pages, write the tree to the XML file
        # and reset the tree / create a new file.
        if page_num % 1000 == 0:
            
            tree._setroot(root)
            fh.write(etree.tostring(tree).decode('utf-8'))
            fh.close()
            
            fh = make_tmpfile(page_num)
            tree = etree.ElementTree()
            root = etree.Element("wikimedia")
        
        # add the 'page' element to the small tree
        root.append(deepcopy(elem))
        #print("appended!!!!!")
        page_num += 1
        

        # release uneeded XML from memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
            
    del context
    #print("deleted context")

def make_tmpfile(pagenum, dir='tempdata'):
    print("creates new file %d" %pagenum)
    '''returns a file object for a small chunk file; must close it yourself'''
    import os
    if not os.path.exists(dir):
        os.mkdir(dir)
        
    fp = os.path.join(dir, 'chunk_%d.xml' % pagenum)
    return  open(fp, mode='w')
    
#get chunks of the data
def final_parser():
    context1 = etree.iterparse("./file1", tag='{http://www.mediawiki.org/xml/export-0.10/}page', encoding='utf-8')
    context2 = etree.iterparse("file2", tag='{http://www.mediawiki.org/xml/export-0.10/}page', encoding='utf-8')

    fast_iter(context1)
    fast_iter(context2)
    et = etree.parse('tempdata')
    root = et.getroot()
    nsmap = {'ns': 'http://www.mediawiki.org/xml/export-0.10/'}

    root.findall('ns:page', nsmap) # find all pages
    root.xpath('*/*/*/ns:username', namespaces=nsmap) # extract all username tags
    root.xpath('ns:page/ns:revision/ns:timestamp', namespaces=nsmap)  # extract all time-stamps

def transform_raw():
    data_holder = {"Page Title": []}
    wiki_set = root.getchildren()

    #to get info from each page

    for each in wiki_set:
        edit_amt = 0
        
        #separate into time and username per edit
        edits_dict = {"Timestamp": [], "Username": [], "Total Number of Edits": []}
        
        for further_info in each:
            if "title" in further_info.tag:
                data_holder["Page Title"].append(further_info.text) 
            if "revision" in further_info.tag:
                
                #keep track of edits per page
                edit_amt = edit_amt + 1
                
                #get time per edit per page
                for edits in further_info:
                    if "timestamp" in edits.tag:
                        edits_dict["Timestamp"].append(edits.text)
                    #get username per edit per page    
                    for user_info in edits:
                        if "username" in user_info.tag:
                            edits_dict["Username"].append(user_info.text)
                            
        #add the total number of edits per page at end of dict
        edits_dict["Total Number of Edits"].append(edit_amt)

        data_holder["Page Title"].append(edits_dict)
    return data_holder
#-------------------------------------------------------------------

#get light dump data
def get_data():
    import zipfile
    import wget

    full_link = 'http://wwm.phy.bme.hu/LD/ld_en_wiki.zip'
    wget.download(full_link, "ld_en_file.zip")

    with zipfile.ZipFile('ld_en_file.zip',"r") as zip_ref:
        zip_ref.extractall("en_light_dump.txt")

#-------------------------------------------------------------------
#number of edits per article
def get_edit_num(file):
    edit_num = {}
    art = file.readline()
    ct = 0

    for i in file:
        if i[0] != "^":
            edit_num[art.rstrip()] = ct
            art = i
            ct = 0
        else:
            ct +=1

    edit_num[art] = ct
    return edit_num