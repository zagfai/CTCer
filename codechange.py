#!/usr/bin/python
# -*- coding: utf-8 -*-
# change the docs code to utf-8 from gbk

import os
import codecs as c

def load_folder(path = os.getcwd() + '/data'):
    folders = [ i.decode('utf8') for i in os.listdir(path)]
    for folder in folders:
        print folder,
        for i in os.listdir(path+'/'+ folder):
            with c.open( path+'/'+folder+'/'+i, 'r', 'gbk', 'ignore') as f:
                t = f.read()
            with c.open( path+'/'+folder+'/'+i, 'w', 'utf-8') as f:
                f.write(t)


if __name__ == '__main__':
    load_folder()
