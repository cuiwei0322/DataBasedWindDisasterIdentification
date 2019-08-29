# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 14:39:13 2019

@author: 95722
"""
import pickle
import pandas as pd
time_period=[0.5,1,3]

def publicnum(num, d = 0):
    dictnum = {}
    for i in range(len(num)):
        if num[i] in dictnum.keys():
            dictnum[num[i]] += 1
        else:
            dictnum.setdefault(num[i], 1)
    maxnum = 0
    maxkey = 0
    for k, v in dictnum.items():
        if v > maxnum:
            maxnum = v
            maxkey = k
    return maxkey
def filePath(filename):
    path='../data/'+filename+'/'
    return path

def isrepete(date,piece):
    if(piece==[]):
        return 1
    else:
        for i in range(len(piece)):
            if(len(piece[i][piece[i]['YR--MODAHRMN'].isin([date])].index)==0):
                return 1
        return 0
        

def piece(data,limit_speed,station):
    piece300=[]
    for i in data.index:
        if(i==0):
            temp=[]
        if(data['SPD'][i]>=limit_speed and isrepete(data['YR--MODAHRMN'][i],piece300)):
            temp.append(data.iloc[i])
            continue
        if(temp!=[]):
            j=0
            l=len(temp)
            while(len(temp)<8):
                temp.insert(0,data.iloc[i-l-j])
                temp.append(data.iloc[i+1+j])
                j=j+1
            temp=pd.DataFrame(temp)
            piece300.append(temp)
        temp=[]
    print('风数据切片完成...')
    #pickle.dump(piece300,open(filePath(station)+'piece.txt','wb'))
    return piece300