import re
import glob
import numpy as np
import warnings
from hmmlearn import hmm
from sklearn.externals import joblib, joblib
import sys
import datetime
from sklearn.mixture import GMM
from sklearn.utils import check_random_state
from sklearn.datasets.samples_generator import make_spd_matrix
import sklearn

from hmmlearn.utils import normalize

value_fuctor = 1.0 # Fuctor for adjasting data

components = 8 # State number of HMM
mix = 10 # Mixture number of GMM

pickup_1 = [42,43,44,45,46,47,48,49,50,51,52,53,60,68,80,92,104]
pickup_2 = [81,82,83,87,88,89,93,94,95,99,100,101,117,131,155,179,203]

motiondata = []
## BVH data ##
for recipe in glob.glob('train\\*'):
    for tool in glob.glob(recipe+'\\*'):
        for file in glob.glob(tool+'\\*.bvh'):
            motiondata.append(file)
print ('motiondata : '+str(len(motiondata)))
resultdata = []
## TXT data ##
for folder in glob.glob('results\\'):
    for txtname in glob.glob(folder+'*.txt'):
        resultdata.append(txtname)

## matching ##
for bvh in motiondata[:]:
    tmpSplit1 = bvh.split('\\')
    tmpbvh = tmpSplit1[3]
    for txt in resultdata[:]:
        tmpSplit2 = txt.split('\\')
        tmptxt = tmpSplit2[1]
        if tmpbvh[:-4] == tmptxt[:-4]:
            # print tmpbvh[:-4]
            motiondata.remove(bvh)

for i in motiondata:
    pathname = []
    motionname = []
    topics = []

    testdata = motiondata.pop(0)
    print('i    : '+str(len(motiondata)))
    print('DATA : '+testdata)

    ## train without testdata ##
    for recipe in glob.glob('train\\*'):
        models = []
        print(recipe[6:])
        pathname.append(recipe[6:])
        m_name = []
        for tool in glob.glob(recipe+'\\*'):
            print(tool[len(recipe)+1:])
            m_name.append(tool[len(recipe)+1:])

            '''
            GMMHMM(algorithm='viterbi', covariance_type='diag', covars_prior=0.01,
                init_params='stmcw', n_components=5, n_iter=10, n_mix=1,
                params='stmcw', random_state=None, startprob_prior=1.0, tol=0.01,
                transmat_prior=1.0, verbose=False)
            '''
            model = hmm.GMMHMM(n_components=components, n_iter=100, n_mix = mix
                                ,verbose=True
                                #,covars_prior=1e-1
                                ,init_params='cmw',params='mctw'
                                ,covariance_type = 'full'
                                #,tol=1e-1
                                )
            '''
            init_params : string, optional
                Controls which parameters are initialized prior to training. Can
                contain any combination of 's' for startprob, 't' for transmat, 'm'
                for means, 'c' for covars, and 'w' for GMM mixing weights.
                Defaults to all parameters.

            params : string, optional
                Controls which parameters are updated in the training process.  Can
                contain any combination of 's' for startprob, 't' for transmat, 'm' for
                means, and 'c' for covars, and 'w' for GMM mixing weights.
                Defaults to all parameters.
            '''
            
            transmat = np.zeros((components,components))

            # Left-to-right: each state is connected to itself and its
            # direct successor.
            ## Correct left-to-right model
            for i in range(components):
                if i == components - 1:
                    transmat[i, i] = 1.0
                else:
                    transmat[i, i] = transmat[i, i + 1] = 0.5

            print(transmat)
            # Always start in first state
            startprob = np.zeros(components)
            startprob[0] = 1.0

            model.transmat_ = transmat
            model.startprob_ = startprob
                    
            gmms = []
            for i in range(0,components):
                gmms.append(sklearn.mixture.GMM())
            model.gmms_ = gmms

            motions = []
            lengths = []
            for file in glob.glob(tool+'\\*.bvh'):
                motion = []
                #print(file)
                count = 0
                if file != testdata:
                    print(file)
                    for line in open(file):
                        if 'MOTION' in line:
                            count+=1
                        elif count > 0:
                            count+=1
                        if count > 4:
                            itemList = line[:-1].split(' ')
                            temppose = []
                            escapes = []
                            if len(itemList) < 200:
                                escapes = pickup_1
                            else:
                                escapes = pickup_2
                            for i,item in enumerate(itemList):
                                try:
                                    float(item)
                                    if(i in escapes):
                                        temppose.append( float(item) * value_fuctor)
                                except Exception as e:
                                    itemList.remove(item)
                            motion.append(temppose)
                    print('motion size :' + str(len(temppose)))
                    motions.append(motion)
                    lengths.append(len(motion))
            X = np.concatenate(motions)
            model.fit(X,lengths)
            print(model.transmat_)
            for line in model.transmat_:
                sum = 0.0
                for one in line:
                    sum += one
                print('sum: ' + str(format(sum,'.15f')))
                if round(sum,4) != 1.0:
                    input('check sum error >>>  ')
            models.append(model)
            joblib.dump(model, tool+'\\'+tool[len(recipe)+1:]+'.pkl')
        topics.append(models)
        motionname.append(m_name)


    ## test mode ##
    print('\n\n--- ' + testdata + ' recognition ---')
    words = testdata.split('\\')
    fileName = words[3]
    print(fileName)
    output = open('results\\'+fileName[:-4]+'.txt','w')
    motion = []
    count = 0
    for line in open(testdata):
        if 'MOTION' in line:
            count+=1
        elif count > 0:
            count+=1
        if count > 4:
            itemList = line[:-1].split(' ')
            temppose = []
            escapes = []
            if len(itemList) < 200:
                escapes = pickup_1
            else:
                escapes = pickup_2
            for i,item in enumerate(itemList):
                try:
                    float(item)
                    if(i in escapes):
                        temppose.append( float(item) * value_fuctor)
                except Exception as e:
                    itemList.remove(item)
            motion.append(temppose)
    scores = []
    topiccount = 0
    for topiccount, topic in enumerate(topics):
        # print ('\n\ntopics'+str(len(topics)))
        # print (topiccount)
        for modelcount, model in enumerate(topic):
            try:
                print(pathname[topiccount]+'['+motionname[topiccount][modelcount]+'] likehood: ' + str(model.score(motion)))
                tmp = [(float(str(model.score(motion)))),pathname[topiccount],motionname[topiccount][modelcount]]
                scores.append(tuple(tmp ))
                output.writelines(str(pathname[topiccount])+'['+str(motionname[topiccount][modelcount])+'] likehood: '+str(model.score(motion))+'\n')
            except Exception as e:
                print(e)
            #print( 'score is ' +  str(model.score(motion)))
    max = -1.0e+15
    index = 0

    print('This motion is estimated to ...')
    ranking = sorted(scores)
    ranking.reverse()
    output.writelines('\n'+'----------RANK----------'+'\n')
    for rank in ranking:
        print(rank)
        output.writelines(str(rank)+'\n')
    output.close()
