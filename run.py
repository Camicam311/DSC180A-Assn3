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


sys.path.insert(0, 'src')
from src.get_m_stat import final_M_stat
from src.etl import get_data


data_params = 'config/data-params.json'
test_params = 'config/test-params.json'

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param


def main(targets):

    if 'data' in targets:
        cfg = load_params(data_params)
        get_data(**cfg)

    if 'test' in targets:
        cfg = load_params(test_params)
        get_data(**cfg)

    if 'calc_m_stat' in targets:
        cfg = load_params(m-stat-param)
        final_M_stat(**cfg)
    
    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)