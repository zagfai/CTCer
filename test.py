#!/usr/bin/python
# -*- coding: utf-8 -*-
# before test you must add folder ./build first.

from tcsys import rw
from tcsys import vec
from tcsys import tsr
from tcsys import knn

def test1():# first test after categorier is created
    T = rw.load_folder()
    print 'example: ',T[0]['cid'],T[0]['categ'],T[0]['filename'],T[0]['str'][:20]

    vec.cutT(T)
    vec.n_gram(T, 2)

    for i in T[0]['sentence'][:10]:
        print i,
    print '\nSize of gram:', len(T[0]['gram'])

    vec.stopwordfilter(T)

    for i in T[0]['stopword'][:5]:
        print i,
    print ' ...\nNow size of gram:', len(T[0]['gram'])

    D,rD = vec.dictify(T)
    rw.write_dict(D, rD)

    for k,v in D.items()[:5]:
        print k,v,
    print ''

    tsr.tfidfctf(T)
    #tsr.x2max_filter(T,D,380,'tfidf')
    tsr.x2max_filter(T,D,380,'tfidf', order='catego')

    test_time = 10
    scl = []
    for i in range(test_time):
        vec.confuse(T)
        #vec.stage_confuse(T, 40)
        #print 't struct',T[0].keys()
        rw.write_libsvm(T,'x2max')
        #rw.write_data(T)
        #rw.write_humanity(T,rD,'tfidf')
        # test return acc, (p,r,f1), [(p,r,f1)]
        scl.append( knn.test(T, 0.8, warn_on_equidistant=False, n_neighbors=10))
    knn.score_analysis(scl)
def test_txt_size_affection():
    import sys
    import codecs as c
    sys.stdout = c.open('result.txtsize', 'w', 'utf8')
    for size in range(650,801,50):
        T = rw.load_folder(size_per_file=size)
        vec.cutT(T)
        vec.n_gram(T, 2)
        vec.stopwordfilter(T)
        D,rD = vec.dictify(T)
        rw.write_dict(D, rD)
        tsr.tfidf(T)
        tsr.x2max_filter(T,D,1000,'tfidf')
        test_time = 100
        scl = []
        for i in range(test_time):
            vec.confuse(T)
            rw.write_libsvm(T,'x2max')
            # test return acc, (p,r,f1), [(p,r,f1)]
            scl.append( knn.test(T, 0.8, warn_on_equidistant=False))
        knn.score_analysis(scl)
def test_stopword_affection():
    import sys
    import codecs as c
    sys.stdout = c.open('result.stopword', 'w', 'utf8')
    T = rw.load_folder()
    vec.cutT(T)
    vec.n_gram(T, 2)
    from copy import deepcopy as dcpy
    rawT = dcpy(T)

    nostf, stf = [], []
    test_time = 100
    for i in range(test_time):
        T = dcpy(rawT)
        vec.confuse(T)
        rw.write_data(T)

        D,rD = vec.dictify(T)
        rw.write_dict(D, rD)
        tsr.tfidf(T)
        tsr.x2max_filter(T,D,1000,'tfidf')
        rw.write_libsvm(T,'x2max')
        nostf.append(knn.test(T, 0.8, warn_on_equidistant=False))

        T = rw.read_T()
        vec.stopwordfilter(T)
        D,rD = vec.dictify(T)
        rw.write_dict(D, rD)
        tsr.tfidf(T)
        tsr.x2max_filter(T,D,1000,'tfidf')
        rw.write_libsvm(T,'x2max')
        stf.append(knn.test(T, 0.8, warn_on_equidistant=False))

    print 'no stop word filtering...'
    knn.score_analysis(nostf)
    print 'stop word filtering...'
    knn.score_analysis(stf)
def test_tfidf():
    T = rw.load_folder()
    vec.cutT(T)
    vec.n_gram(T, 2)
    vec.stopwordfilter(T)
    D,rD = vec.dictify(T)
    rw.write_dict(D, rD)
    tsr.tfidf(T)
    tsr.x2max_filter(T,D,100000,'tfidf')
    rw.write_humanity(T,rD,'x2max')
def test_dimension_affection():
    T = rw.load_folder()
    vec.cutT(T)
    vec.n_gram(T, 2)
    vec.stopwordfilter(T)
    D,rD = vec.dictify(T)
    rw.write_dict(D, rD)
    tsr.tfidfctf(T)
    rw.write_data(T)

    test_time = 20
    rang = range(40, 1001, 40)
    scl = {}
    for i in rang:
        scl[ i ] = []
    for i in range(test_time):
        vec.confuse(T)
        for dimen in rang:
            print dimen
            tsr.x2max_filter(T,D,dimen,'tfidf')
            rw.write_libsvm(T,'x2max')
            # test return acc, (p,r,f1), [(p,r,f1)]
            acc,(_,_,f1),_ = knn.test(T, 0.8, warn_on_equidistant=False)
            scl[dimen].append((acc,f1))
    print scl
    for dimen in rang:
        print dimen,'acc:',sum([ i[0] for i in scl[dimen]])/ float(test_time),\
                    'f1 :',sum([ i[1] for i in scl[dimen]])/ float(test_time)
def test_bigdata():
    T = rw.load_folder()
    vec.cutT(T)
    vec.n_gram(T, 2)
    vec.stopwordfilter(T)
    D,rD = vec.dictify(T)

    tsr.tfidfctf(T)
    tsr.x2max_filter(T,D,380,'tfidf', order='catego')
    del D
    del rD
    for t in T:
        del t['tfidf']
        del t['gram']

    test_time = 10
    proportions = [.2, .4, .6, .8] + range(1,10)
    scl = { proportion:[] for proportion in proportions }
    for i in range(test_time):
        vec.confuse(T)
        #vec.stage_confuse(T, 40)
        rw.write_libsvm(T,'x2max')
        # test return acc, (p,r,f1), [(p,r,f1)]
        for proportion in proportions:
            scl[proportion].append( knn.test(T,proportion/10.0, algorithm='kd_tree', warn_on_equidistant=False, n_neighbors=10))
    for p in proportions:
        print 'proportion:',p,'......................................'
        knn.score_analysis(scl[p], outitem='af', outdetail=False)
def test_k():
    T = rw.load_folder()
    vec.cutT(T)
    vec.n_gram(T, 2)
    vec.stopwordfilter(T)
    D,rD = vec.dictify(T)
    tsr.tfidfctf(T)
    tsr.x2max_filter(T,D,400,'tfidf', order='catego')


    test_time = 5
    kval = range(1, 101)
    scl = { k:[] for k in kval}
    for i in range(test_time):
        vec.confuse(T)
        rw.write_libsvm(T,'x2max')
        for k in kval:
            scl[k].append( knn.test(T, 0.8, weights='distance', warn_on_equidistant=False, n_neighbors=k))
    print 'A:',
    for k in kval:
        print sum([ i[0] for i in scl[k]])/test_time,
        #knn.score_analysis(scl[k], outitem='af', outdetail=False)
    print ''
    print 'F:',
    for k in kval:
        print sum([ i[1][2] for i in scl[k]])/test_time,

def test_it():
    T = rw.load_folder()
    vec.cutT(T)
    vec.n_gram(T, 2)
    vec.stopwordfilter(T)
    D,rD = vec.dictify(T)
    tsr.tfidf(T)
    #tsr.x2max_filter(T,D,380,'tfidf')
    tsr.x2max_filter(T,D,1000,'tfidf', order='catego')
    #rw.write_dict(D, rD)
    #rw.write_humanity(T,rD)

if __name__ == '__main__':
    test1()
    #test_knn()
    #test_k()
    #test_bigdata()
    #test_it()
