#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:43:09 2020

@author: francois
"""
from collections import Counter
from operator import itemgetter 
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
import numpy as np
import pandas as pd
from taskfunctions import clean_imname
from taskfunctions import flatten
from taskfunctions import get_datas
from taskfunctions import get_synsets
from tree import tree
IMDIR = '../images'

class ImageBank():
    ''' Courtois-Neuromod Image Bank
    '''
    def __init__(self, imdir):
        self.syns = get_synsets()
        self.datas = get_datas(imdir)
        self.images = self.get_images()
        self.folders = self.get_folders()
        self.im_vectors = self.get_im_vecs()
        self.categories = self.get_categories()
        self.word_freqs = self.get_word_freqs()

    def get_categories(self):
        ''' Description
            -----------
            Gathers each item in self.datas belonging to each category.\
            Would be another part of the pd.MultiIndex.\
            Imported Method(s)
            ------------------
            get_syns()
            Variables
            ---------
            syns: see help(get_syns)
            Returns
            -------
            ImageBank.categories:\
                dict object\
                    keys = categories\
                    values = DF containing each image_concept\
                             in self.datas belonging to each category (key)
        '''
        categories = dict(((syn[0], pd.DataFrame.from_dict(\
                                    dict((row for row in pd.concat([self.images,
                                                                    self.folders], levels=['face', 'body']).iterrows()
                                          if syn[0] in row[1]['tags'] and\
                                              len(row[1]['subordinates']) == 0)),
                                    orient='index').transpose())
                           for syn in self.syns.iterrows()))
        return categories

    def get_word_freqs(self):
        ''' Description
            -----------
            Returns a Counter object counting how often each synset appears\
            in the database, either as image, category, tag, subordinate.
        '''
        return pd.Series(dict(Counter(flatten(self.datas.freq_tags)))).sort_index()

    def get_folders(self):
        ''' Description
            -----------
        '''
        folders = pd.DataFrame((row[1]for row in self.datas.iterrows()
                               if not all(pd.isnull(row[1]['subordinates']))),
                              columns=list(self.datas.columns))
        folders['names'] = [bname(folders.loc[ind]['path'])
                           for ind in folders.index]
        folders = folders.set_index('names')
        folders = folders.sort_index(kind='mergesort')
        return folders

    def get_images(self):
        ''' Description
            -----------
            DF containing each image_concept\
            Returns
            -------
            ImageBank.images
        '''
        images = pd.DataFrame((row[1]for row in self.datas.iterrows()
                               if pd.isnull(row[1]['subordinates']).all()),
                              columns=list(self.datas.columns))
        # images['names'] = ['_'.join([bname(row[1]['path']),
        #                              bname(dname(row[1]['path']))])
        #                    for row in images.iterrows()]
        images['names'] = [bname(row[1]['path']) for row in images.iterrows()]
        images = images.set_index('names')
        images = images.sort_index(kind='mergesort')
        return images
    
    def get_im_vecs(self):
        '''Description
           -----------
           DF containing a an array indexing each image_concept in CNIB\
           with values being either\
               0 :image_concept not in category\
               1 :image_concept in category\
           Returns
           -------
           "Potentially a great pd.MultiIndex?, to be implemented...
           Not very useful at the moment."
           '''
        return pd.DataFrame(np.array([[int(im_tags.__contains__(tag))
                                       for tag in self.syns.index]
                                      for im_tags in self.datas['tags']]),
                            columns=self.syns.index, index=self.datas.index)

# DATAS = CNIB.datas
# IMAGES = CNIB.images
# FOLDERS = CNIB.folders
# CATEGORIES = CNIB.categories
# SYNS = get_synsets()
# IM_VECTORS = CNIB.get_im_vecs()
# WORD_FREQS = CNIB.word_freqs
toplevel = [join(IMDIR, item) for item in os.listdir(IMDIR)]
sub1 = [os.listdir(top) for top in toplevel]
toptest = list(zip(toplevel, sub1))
subpaths = [[join(top, sub) for sub in sub1] for top in toplevel]
datas = [get_datas(item) for item in toplevel]
CNIB = ImageBank(imdir=IMDIR)

datas = CNIB.datas
categories = CNIB.categories
images = CNIB.images
folders = CNIB.folders
# syns = get_synsets()
im_vectors = CNIB.get_im_vecs()
word_freqs = CNIB.word_freqs

def bigdata(datas):
    catlst = pd.DataFrame(((bname(fpath), pd.DataFrame((pd.Series(row[1], 
                                                                  name=row[0],
                                                                  index=row[1].index)
                                                        for row in get_datas(fpath).iterrows())))
                              for fpath in datas.path)).set_index(0)
    return catlst
    # midx = pd.MultiIndex.from_tuples(datalst, names =('category', 'datas')) 
    # final = pd.DataFrame(((item[0], item[1]) for item in datalst.items()),
    #                      index=[item[0] for item in datalst.items()])
big3 = bigdata(folders).fillna('nan')
# test = bigdata(animals)
# test = pd.DataFrame.from_dict(categories, orient='index')
# def big(datas):
#     for subs in datas.subordinates:
#         sublist = []
#         for imname in datas['names']:
#             for sub in subs:
#                 if sub in imname:
#                     sublist.append((sub, datas.loc[imname]))
#         datas['sublist'] =  sublist
#     return datas
# bigdatas = big(images)
          
# test3 = [(item[0],
#           [row for row in IMAGES.iterrows()
#            if str(dname(row[1].path)) == str(FOLDERS.loc[item[0]]['path'])])
#          for item in FOLDERS.transpose().iteritems()]
# test9 = [(item[0], [(row[0], row[1]) for row in IMAGES.iterrows()
#                     if str(dname(row[1].path)) == \
#                         str(FOLDERS.loc[item[0]]['path'])])
#           for item in FOLDERS.transpose().iteritems()]
# test12 = [pd.DataFrame((item[0], pd.Series((pd.Series(row[1].values, name=row[0], index=row[1].index) for row in IMAGES.iterrows()
#                     if str(dname(row[1].path)) == \
#                         str(FOLDERS.loc[item[0]]['path'])), name=item[0], index=item[1].index).transpose()))
#           for item in FOLDERS.transpose().iteritems()]
# test9_2 = [(item[0], [(row[0], row[1]) for row in IMAGES.iterrows()
#                     if str(dname(row[1].path)) == \
#                        str(FOLDERS.loc[item[0]]['path'])])
#          for item in FOLDERS.transpose().iteritems()]

# test4 = [(item[0],
#           [pd.Series(row[1], name=row[0], index=row[1].index) for row in IMAGES.iterrows()
#            if str(dname(row[1].path)) == str(FOLDERS.loc[item[0]]['path'])])
#          for item in FOLDERS.transpose().iteritems()]
# test5 = [pd.DataFrame((item[0],
#           [pd.Series(row[1], name=row[0], index=row[1].index) for row in IMAGES.iterrows()
#            if str(dname(row[1].path)) == str(FOLDERS.loc[item[0]]['path'])]))
#          for item in FOLDERS.transpose().iteritems()]

# test6 = [pd.DataFrame((item[0],
#           [pd.Series(row[1], name=row[0], index=row[1].index).transpose() for row in IMAGES.iterrows()
#            if str(dname(row[1].path)) == str(FOLDERS.loc[item[0]]['path'])])).transpose()
#          for item in FOLDERS.transpose().iteritems()]

# test7 = [pd.DataFrame((item[0],
#           pd.DataFrame(pd.Series(row[1], name=row[0], index=row[1].index).transpose() for row in IMAGES.iterrows()
#            if str(dname(row[1].path)) == str(FOLDERS.loc[item[0]]['path'])))).transpose()
#          for item in FOLDERS.transpose().iteritems()]
# test8 = [pd.DataFrame((item[0],
#           pd.DataFrame((row[0], pd.Series(row[1], name=row[0],
#                                  index=row[1].index).transpose())
#                        for row in IMAGES.iterrows()
#                        if str(dname(row[1].path)) == str(FOLDERS.loc[item[0]]['path'])).transpose())).transpose()
#          for item in FOLDERS.transpose().iteritems()]