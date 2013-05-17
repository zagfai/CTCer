#!/usr/bin/python
# -*- coding: utf-8 -*-

import rw
import math

# tfidf funcs
def tfidf_word(word_time, words_count, doct_all, doct_word_display):
    tf = float(word_time) / words_count
    idf = math.log( float(doct_all) / doct_word_display)
    return tf*idf
def idf_dict(T):
    print 'building idf ...',
    doct_word_display = {}
    for t in T:
        for k in t['gram'].keys():
            doct_word_display[k] = doct_word_display.get(k,0) + 1
    print 'finish'
    return doct_word_display
def tfidf(T):
    text_all_size = len(T)
    doct_word_display = idf_dict(T)
    print 'start counting tfidf...',
    for t in T:
        t['tfidf'] = {}
        for k in t['gram'].keys():
            t['tfidf'][k] = tfidf_word( t['gram'][k], sum(t['gram'].values()),
                                  text_all_size, doct_word_display[k])
    print 'finish.'
    return T
def tfidfctf(T):
    text_all_size = len(T)
    doct_word_display = idf_dict(T)
    print 'start counting tfidfctf for tf...',
    wordinc = {}
    sumwordinc = {}
    for t in T:
        for k in t['gram'].keys():
            wordinc[ t['cid'], k ] = wordinc.get((t['cid'], k),0) + t['gram'][k]
            sumwordinc[ t['cid'] ] = sumwordinc.get(t['cid'], 0) + t['gram'][k]
    for t in T:
        t['tfidf'] = {}
        for k in t['gram'].keys():
            t['tfidf'][k] = tfidf_word( t['gram'][k], sum(t['gram'].values()),
                                  text_all_size, doct_word_display[k])
            t['tfidf'][k] *= 1000 * wordinc[ t['cid'], k] / float(sumwordinc[ t['cid']])
            # ctf-idf
            #t['tfidf'][k] = tfidf_word( wordinc[t['cid'],k], float(sumwordinc[ t['cid']]),
            #                      text_all_size, doct_word_display[k])
    print 'finish.'
    return T

# chi2 algo funcs
def chi2(A, B, C, D):
    sup = (A+C) * (B+D) * (A+B) * (C+D)
    if sup <= 0:
        return 0
    else:
        return float( (A*D - B*C)**2 )/sup
def A_dict(T):
    print 'building A_dict... ',
    tc_dict = {}
    for t in T:
        cid = t['cid']
        for w in t['gram'].keys():
            tc_dict[(w,cid)] = tc_dict.get((w,cid),0) + 1
            tc_dict[(w,'sum')] = tc_dict.get((w,'sum'),0) + 1
    print 'size: ',len(tc_dict)
    return tc_dict
def x2calc(T,D):
    ass = A_dict(T)
    dpc = {}
    for t in T:
        dpc[ t['cid'] ] = dpc.get( t['cid'], 0) + 1
    sizeT = len(T)
    print 'counting X2 for words to category...',
    for ww,pb in D.items():
        wid = pb['wid']
        x2l = []
        for cid in sorted(dpc.keys()):
            A = ass.get((wid,cid),0)
            B = ass.get((wid,'sum'),0) - A
            x2l.append( chi2(A, B, dpc[cid]-A, (sizeT-dpc[cid])-B) )
        D[ww]['x2l'] = x2l
    print 'finish.'
    return D
def x2max_filter(T,D, size=10, val='gram', order='max'):
    x2calc(T,D)
    print 'x2max (gram_size=',size,'val=',val,'order=',order,')...',
    ccc = len(set([ t['cid'] for t in T ])) # count the catogries kinds
    dl = []
    for w in D.itervalues():
        dl.append((w['wid'], max(zip(w['x2l'], range(1,ccc+1)), key= lambda x:x[0] )))
    dl.sort(key = lambda x:x[1], reverse=True)

    if order == 'catego':
        dl_cls = [ [] for i in range(ccc+1) ]
        for word in dl:
            dl_cls[ word[1][1] ].append( word )
        spc = size/ccc
        dl = reduce((lambda x,y:x+y[:spc]), dl_cls)

    dd = { i[0]:1 for i in dl[:size] }
    #data filtering
    if dd == None or dd == {}:
        raise Exception
    for t in T:
        t['x2max'] = {}
        for w in t['gram']:
            if w in dd:
                t['x2max'][w] = t[val][w]
    print 'finish.'
    return T


def test():
    T,D,rD = rw.read_data()
    x2max_filter(T,D,1000,'tfidf')
    #rw.write_humanity(T,rD,'x2max')
    #rw.write_libsvm(T,'x2max')
if __name__ == '__main__':
    test()
