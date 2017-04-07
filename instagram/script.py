#! usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os.path import exists
import simplejson as json 
import pysal
import numpy as np
import shapefile as sp
import math
import clusterpy as cp
import csv
import sklearn.decomposition as sc
from sklearn.feature_selection import SelectKBest