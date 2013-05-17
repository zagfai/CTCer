#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs as c
import cPickle as pk
import re

def cutt(t):
    # 清除不分段符号
    repdic = (  (u'　',''),
                (' ', ''),
                (u'“',''),
                (u'”',''),
                (u'‘',''),
                (u'’',''),
                (u'（',''),
                (u'）',''),
                (u'【',''),
                (u'】',''),
                # en's
                (u'"',''),
                (u'\'',''),
                (u'/',''),
                (u'*',''),
                (u'(',''),
                (u')',''),
    )
    t['str'] = reduce( (lambda tt,rp: tt.replace( rp[0], rp[1])), (t['str'],) + repdic)
    # 分段符号化为空格
    cutdic = (  (u'，',' '),
                (u'。',' '),
                (u'！',' '),
                (u'？',' '),
                (u'：',' '),
                (u'、',' '),
                (u'；',' '),
                (u'《',' '),
                (u'》',' '),
                (u'〕',' '),
                (u'〔',' '),
                # en's
                (u':',' '),
                (u'/',' '),
                (u'!',' '),
                (u'?',' '),
                (u',',' '),
                (u';',' '),
            )
    t['str'] = reduce( (lambda tt,rp: tt.replace( rp[0], rp[1])), (t['str'],) + cutdic)
    # 半角化
    def Q2B(uchar):
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:
            return uchar
        return unichr(inside_code)
    # 字母小写化 和 半角化
    t['str'] = ''.join([ Q2B(i.isupper() and i.lower() or i) for i in t['str']])
    # 清除字母及百分比
    t['str'] = re.sub(r'([0-9.]+)[ ]*%*', ' ', t['str'])
    t['str'] = re.sub(r'\s+', ' ', t['str'])
    t['sentence'] = t['str'].split()
    return t
def cutT(T):
    print 'start cutting text to sentences... ',
    for t in T:
        cutt(t)
        #print t['cid'],
    print 'finish.'
def n_gram(T, gram):
    print 'gramming...',
    for t in T:
        t['gram'] = {}
        new_s = []
        for piece in t['sentence']:
            for pos in range(len(piece)-gram+1):
                w = piece[ pos:pos+gram]
                new_s.append(w)
                t['gram'][w] = t['gram'].get(w,0) + 1
            t['sentence'] = new_s
    print 'finish.'
def stopwordfilter(T):
    print 'stop working... what??',
    with c.open('stop', 'r', 'utf-8') as f:
        sw = f.readlines()
    sw_dict = {}
    for i in [ i[:-1] for i in sw ]:
        sw_dict[i] = 1
    for t in T:
        t['stopword'] = []
        for k in t['gram'].keys():
            if sw_dict.has_key(k):
                t['gram'].pop(k,0)
                t['stopword'].append(k)
    print 'stopwords out, aha.'
# make dictionary as { {w:{wid,scores} }
def dictify(T):
    print 'building dictionary and make t["gram"] numeric...',
    D = {}
    rD = {}
    top = 0
    for t in T:
        for k in t['gram'].keys():
            if not D.has_key(k):
                D.update({k:{'wid':top}})
                top += 1
            t['gram'][ D[k]['wid'] ] = t['gram'].pop(k)
    for word,prob in D.items():
        rD[ prob['wid'] ] = word
    print 'size:',len(D),'finish.'
    return D,rD
#TODO
def wordify(T):
    pass
def confuse(T):
    print 'confusing data...',
    from random import random as r
    size = len(T)
    for i in range(int(size**1.5)):
        x,y = int(size*r()), int(size*r())
        T[x], T[y] = T[y], T[x]
    print 'finish.'
    return T
def stage_confuse(T, trainning_size_per_categ=50):
    '''take trainning set in the front of T.'''
    print 'staging...',
    size = trainning_size_per_categ
    cd = {}
    lf = []
    for t in T[:]:
        cid = t['cid']
        if cd.has_key(cid):
            if len(cd[cid]) < size:
                cd[cid].append(t)
            else:
                lf.append(t)
        else:
            cd[cid] = [t,]
        T.remove(t)
    for l in cd.values():
        T.extend(l)
    T.extend(lf)
    print 'finish.'
    return T

