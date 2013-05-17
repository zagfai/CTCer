#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
import codecs as c
import cPickle as pk

def load_folder(path = os.getcwd() + '/data', size_per_file=200):
    print 'reading data...'
    folders = [ i.decode('utf8') for i in os.listdir(path)]
    T = []
    cls = 0
    for folder in folders:
        cls +=1 # data category
        print folder,
        for i in os.listdir(path+'/'+ folder):
            with c.open( path+'/'+folder+'/'+i, 'r', 'utf8') as f:
                t = f.read().replace('&nbsp;',' ').replace('\n',' ').\
                        replace('&amp','').replace('\r',' ').replace('\n',' ').\
                        replace('--',' ').replace(u'　',' ').replace('~', ' ')
                t = re.sub(r'\s+', '', t)
                start_pos = (len(t)-size_per_file) / 2
                if start_pos < 0:
                    start_pos = 0
                T.append({'cid':cls, 'categ':folder, 'filename':i,
                    'str':t[ start_pos : start_pos+size_per_file]})
                #print T[-1]['cid'],T[-1]['categ'],T[-1]['str']
    print '\nfinish. size of T:',len(T)
    return T
def write_data(T):
    print 'writing data files......',
    with open('build/T.dat', 'w') as fw:
        pk.dump(T,fw)
    print 'finish.'
def write_libsvm(T, weight='gram'):
    print 'writing T.libsvm as ' + weight + '...',
    fw = c.open('build/T.libsvm', 'w', 'utf-8')
    for t in T:
        fw.write(str(t['cid']))
        for i in sorted(t[weight].items(), key=lambda x:x[0]):
            fw.write( u' ' + str(i[0]) + u':' + str(i[1]))
        fw.write('\n')
    print 'finish.'
    return fw
def write_humanity(T,rD, weight='gram'):
    print 'writing T readable as ' + weight + '...',
    with c.open('build/T.txt', 'w', 'utf-8') as fw:
        for t in T:
            fw.write(str(t['cid'])+' '+t['categ']+' '+t['filename'][:-4] + '\t')
            for i in sorted(t[weight].items(), key=lambda x:x[1], reverse=True):
                fw.write( u' ' + rD[i[0]] + u':' + str(round(i[1],3)))
            fw.write('\n')
    print 'finish.'
def write_dict(D,rD):
    print 'writing dict...',
    with open('build/D.dat', 'w') as fw:
        pk.dump(D,fw)
    with open('build/rD.dat', 'w') as fw:
        pk.dump(rD,fw)
    with c.open('build/D.txt', 'w', 'utf-8') as fw:
        fw.writelines([ i[0] + ' ' + str(i[1]) + '\n'
                for i in sorted(D.items(), key=lambda x:x[1]['wid'])])
    print 'finish.'
def read_data():
    print 'reading data files......',
    with open('build/D.dat') as f:
        D = pk.load(f)
    with open('build/rD.dat') as f:
        rD = pk.load(f)
    with open('build/T.dat') as f:
        T = pk.load(f)
    print 'finish.'
    return T,D,rD
def read_T():
    print 'reading T......',
    with open('build/T.dat') as f:
        T = pk.load(f)
    print 'finish.'
    return T


if __name__ == '__main__':
    load_folder()
