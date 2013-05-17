#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn import neighbors as nb
from sklearn.datasets import load_svmlight_file
import rw

def scores(a,y,T, outp=True):
    '''score func, score(a,y,T,outp=True) which take "a" as predict class, "y" as true class(list), T as the TextStruct and output or return the score of the classfier.'''
    size = len(y)
    correct = sum([ a[i] == y[i] for i in range(size)])
    acc = round( correct/float(size), 3)
    if outp == True:
        print 'correct rate:',acc
        print 'cc\tp\tr\tf1'
    ccc = len(set([ t['cid'] for t in T ])) # count the catogries kinds
    eva = []
    for cc in range(1,ccc+1):
        A = len([ i for i in range(size) if a[i]==cc and cc==y[i] ])
        B = len([ i for i in range(size) if a[i]==cc and cc!=y[i] ])
        C = len([ i for i in range(size) if a[i]!=cc and cc==y[i] ])
        p = r = 0.00001
        try:
            p = float(A)/(A+B)
            r = float(A)/(A+C)
        except:
            pass
        # precision, recall, F1
        eva.append(( round(p,3), round(r,3), round(2*p*r/(p+r+0.00001), 3)))
        if outp == True:
            print cc,'\t',eva[-1][0],'\t',eva[-1][1],'\t',eva[-1][2]
    v = ( sum([ i[0] for i in eva])/ccc,
          sum([ i[1] for i in eva])/ccc,
          sum([ i[2] for i in eva])/ccc)
    if outp == True:
        print 'avg-p:', v[0],
        print 'avg-r:', v[1],
        print 'avg-f1:',v[2],
    return acc, v, eva
def score_analysis(scl, outitem='aprfc', outdetail=True):
    '''analysis the scores list, and control the output format.'''
    print 'Score analysis report.'

    ccc = len(scl[0][2])
    count_avg = lambda pos: round( sum([ eva[cc][pos] for eva in evall])/len(evall), 3 )
    def print_avg(tit, lt):
        print tit,
        if outdetail:
            for i in lt:
                print i,
            print ''
        print 'max:',max(lt),'min:',min(lt),'avg:',float(sum(lt))/len(scl)
    accl, pl, rl, fl, evall = [], [], [], [], []
    for sc in scl:
        acc, prf, eva = sc
        accl.append(acc)
        pl.append(prf[0])
        rl.append(prf[1])
        fl.append(prf[2])
        evall.append(eva)

    # print !
    if 'a' in outitem:
        print_avg( 'A: ', accl)
    if 'p' in outitem:
        print_avg( 'P: ', pl)
    if 'r' in outitem:
        print_avg( 'R: ', rl)
    if 'f' in outitem:
        print_avg( 'F: ', fl)

    if 'c' in outitem and outdetail:
        print 'cc\tp\tr\tf1 (in avg)'
        for cc in range(ccc):
            avg_p = count_avg(0)
            avg_r = count_avg(1)
            avg_f = count_avg(2)
            print cc+1,'\t',avg_p,'\t',avg_r,'\t',avg_f
def test(T,train_size, load_file='build/T.libsvm', algorithm='auto',
         leaf_size=30, n_neighbors=10, p=2,
         warn_on_equidistant=True, weights='uniform'):
    '''test layer base on sklearn neighbors'''
    if type( train_size ) is float and train_size < 1:
        train_size = train_size * len(T)
    train_size = int(train_size)
    print 'knn testing, train set take',train_size*100/float(len(T)),'%...'
    print 'train set size:',train_size,'T size:',len(T)
    X,y = load_svmlight_file(load_file)
    #knn = nb.nearest_centroid.NearestCentroid()
    knn = nb.KNeighborsClassifier(
            algorithm=algorithm, leaf_size=leaf_size, n_neighbors=n_neighbors,
            p=p, warn_on_equidistant=warn_on_equidistant, weights=weights)
    knn.fit(X[:train_size],y[:train_size])
    a = knn.predict(X[train_size:]).tolist()
    return scores(a,y[train_size:],T,warn_on_equidistant)

if __name__ == '__main__':
    T,_,_ = rw.read_data()
    test(T, .8, load_file='/tmp/T.libsvm', warn_on_equidistant=True)
