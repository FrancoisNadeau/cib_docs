#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 16:51:03 2020

@author: francois
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 01:26:09 2020

@author: francois
"""
from collections import Counter
from operator import itemgetter
import os
from os.path import basename as bname
from os.path import dirname as dname
from os.path import join
from os import listdir as ls
import numpy as np
import pandas as pd
from taskfunctions import clean_imname
from taskfunctions import flatten
from taskfunctions import get_datas
from taskfunctions import get_synsets
from taskfunctions import loadimages
from tree import tree
IMDIR = '../images'

class ImageBank():
    ''' Courtois-Neuromod Image Bank
    '''
    def __init__(self, imdir):
        self.syns = get_synsets()
        self.datas = get_datas(imdir)
        self.images = self.datas[2]
        self.folders = self.datas[1]
        # self.im_vectors = self.get_im_vecs()
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
                                                                    self.folders]).iterrows()
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
        return pd.Series(dict(Counter(flatten(self.datas[0].freq_tags)))).sort_index()
CNIB = ImageBank(imdir=IMDIR)
datas, folders, images = CNIB.datas
# categories = CNIB.categories
# images = CNIB.images
# folders = CNIB.folders
# syns = get_synsets()
# im_vectors = CNIB.get_im_vecs()
word_freqs = CNIB.word_freqs

levels = pd.DataFrame(folders['subs'])
ld = dict(levels)
ldf = pd.DataFrame.from_dict(ld, orient='index')
lowlevel2 = pd.DataFrame(([pd.DataFrame((bname(item),
                                         pd.DataFrame((bname(item), len(ls(item)),
                                         pd.DataFrame((img, (len(ls(join(item, img))),
                                                             ls(join(item, img)))) for img in ls(item)
                                                      if os.path.isdir(join(item,img))))))).transpose().set_index(0).squeeze()
                           for item in row[1]['subs']]
                          for row in folders.iterrows()), index=folders.index)
lowlevel3 = lowlevel2.drop([row[0] for row in lowlevel2.iterrows()
                            if '.jpg' not in str(row[1].values)])
lowlevel4 = lowlevel2.drop(lowlevel3.index)
ntop = lowlevel4
nbot = lowlevel3
ndatas = lowlevel2
ndatas.to_excel('../docs/A_newdatas_clean.xlsx')
nbot.to_excel('../docs/A_newimages.xlsx')
ntop.to_excel('../docs/A_newfolders.xlsx')
# lowlevel6 = lowlevel4.replace(lowlevel4.values, pd.DataFrame((val for val in lowlevel4.values)))
# lowlevel5 = [pd.DataFrame(pd.Series((value))) for value in lowlevel4.values]
# low4 = [pd.DataFrame((row[0], row[1].valueslowlevel4[]
def get_final(nbot, ntop):
    ncp = ntop
    test=[]
    for toprow in ntop.iterrows():
        for val in toprow[1]:
            test.append((toprow[0], pd.DataFrame(val)))
    return test
# test3 = np.array([pd.DataFrame(val) for val in ntop.values])
# testa = get_final(nbot, ntop)    
# pd.DataFrame((pd.DataFrame(val) for val in ntop.values), index=ntop.index)      
    # def get_folders(self):
    #     ''' Description
    #         -----------
    #     '''
    #     folders = pd.DataFrame((row[1]for row in self.datas.iterrows()
    #                            if not all(pd.isnull(row[1]['subordinates']))),
    #                           columns=list(self.datas.columns))
    #     folders['names'] = [bname(folders.loc[ind]['path'])
    #                        for ind in folders.index]
    #     folders = folders.set_index('names')
    #     folders = folders.sort_index(kind='mergesort')
    #     return folders

    # def get_images(self):
    #     ''' Description
    #         -----------
    #         DF containing each image_concept\
    #         Returns
    #         -------
    #         ImageBank.images
    #     '''
    #     images = pd.DataFrame((row[1]for row in self.datas.iterrows()
    #                            if pd.isnull(row[1]['subordinates']).all()),
    #                           columns=list(self.datas.columns))
    #     # images['names'] = ['_'.join([bname(row[1]['path']),
    #     #                              bname(dname(row[1]['path']))])
    #     #                    for row in images.iterrows()]
    #     images['names'] = [bname(row[1]['path']) for row in images.iterrows()]
    #     images = images.set_index('names')
    #     images = images.sort_index(kind='mergesort')
    #     return images
    
    # def get_im_vecs(self):
    #     '''Description
    #        -----------
    #        DF containing a an array indexing each image_concept in CNIB\
    #        with values being either\
    #            0 :image_concept not in category\
    #            1 :image_concept in category\
    #        Returns
    #        -------
    #        "Potentially a great pd.MultiIndex?, to be implemented...
    #        Not very useful at the moment."
    #        '''
    #     return pd.DataFrame(np.array([[int(im_tags.__contains__(tag))
    #                                    for tag in self.syns.index]
    #                                   for im_tags in self.datas['tags']]),
    #                         columns=self.syns.index, index=self.datas.index)
# DATAS = CNIB.datas
# IMAGES = CNIB.images
# FOLDERS = CNIB.folders
# CATEGORIES = CNIB.categories
# SYNS = get_synsets()
# IM_VECTORS = CNIB.get_im_vecs()
# WORD_FREQS = CNIB.word_freqs
# toplevel = [join(IMDIR, item) for item in ls(IMDIR)]
# sub1 = [ls(top) for top in toplevel]
# toptest = list(zip(toplevel, sub1))
# subpaths = [[join(top, sub) for sub in sub1] for top in toplevel]
# datas = [get_datas(item) for item in toplevel]


# level3 = [[(bname(subpath), ls(subpath)) for subpath in row[1].subs]
#                   for row in pd.DataFrame(levels).iterrows()]
# for frow in folders.iterrows():
#     for imrow in images.iterrows():
#         subfolders = dict(zip((frow[1].subordinates, imrow[1].path) if imrow[1].path == )
#         for subpath in frow[1].subs:
#             if subpath == imrow[1].path:
                
        
# botlvl = sorted(list(dict.fromkeys([(bname(dname(item)), dname(item)) for item in loadimages()])))
# bottom_d = pd.DataFrame(botlvl).set_index(0)
# bottom_d['imnames'] = [ls(row[1][1]) for row in bottom_d.iterrows()]

# imlvl = [b for ind in lowlevel2.index if lowlevel2[ind]]
# toplevel = [join(IMDIR, item) for item in ls(IMDIR)]

          
# def bigdata(datas):
#     catlst = pd.DataFrame(((bname(fpath), pd.DataFrame((pd.Series(row[1], 
#                               e                                    name=row[0],
#                                                                   index=row[1].index)
#                                                         for row in get_datas(fpath).iterrows())))
#                               for fpath in datas.path)).set_index(0)
#     return catlst
#     midx = pd.MultiIndex.from_tuples(catlst, names =('category', 'datas')) 
#     # final = pd.DataFrame(((item[0], item[1]) for item in datalst.items()),
#     #                      index=[item[0] for item in datalst.items()])
# big3 = bigdata(folders).fillna('nan')
