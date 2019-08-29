# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:44:47 2019

@author: 95722
"""

import pandas as pd
import numpy as np
import pickle
import time
import toughness
import os


target=['USAF','YR--MODAHRMN','TEMP','DEWP']
            
    
def data_pre(data,target):
    da={}
    for i in target:
        da[i]=data[i]
    ndata=pd.DataFrame(da)
    return ndata
        
#降水量处理 处理为过去3小时降雨量 单位毫米
def pcp_pre(data):
    pcp=data['PCP06']
    pcp=pcp.replace('*****',np.nan)
    pcp=pcp.replace('0.00T*****',np.nan)
    pcp=pcp.replace('0.00T',np.nan)
#转换数据格式为浮点数
    pcp=pd.to_numeric(pcp)
#线性插值方法处理中间空值
    for i in range(len(pcp)):
        if(np.isnan(pcp[i])):
            pcp[i]=0
        

            if(i==0 and np.isnan(pcp[i+1])):
                pcp[i]=0
                continue
            if(i==len(pcp)-1):
                pcp[i]=pcp[i-1]/2
                break
            if(not((np.isnan(pcp[i-1]))or(np.isnan(pcp[i+1])))):
                pcp[i]=(pcp[i-1]+pcp[i+1])/2
            else:
                pcp[i]=0
 
        
#单位转换：英寸->毫米
    for i in range(len(pcp)):
        pcp.iloc[i]=pcp.iloc[i]*25.4*1.5
        
    return pcp
        

def slp_pre(data):
    slp=data['SLP']
    alt=data['ALT']
    slp=slp.replace('*****',np.nan)
    slp=slp.replace('******',np.nan)
    alt=alt.replace('*****',np.nan)
    alt=alt.replace('******',np.nan)
    slp=pd.to_numeric(slp)
    alt=pd.to_numeric(alt)
    for i in range(len(slp)):
        if(np.isnan(slp[i])):
            slp.iloc[i]=round(alt[i],1)
            
        if(np.isnan(slp[i])):
            slp.iloc[i]=round((slp[i-1]+slp[i-1])/2,1)
    return slp

def Wind_pre(data):
    Dir=data['DIR']
    Spd=data['SPD']
    Dir=Dir.replace('***',np.nan)
    Spd=Spd.replace('***',np.nan)
    Dir=pd.to_numeric(Dir)
    Spd=pd.to_numeric(Spd)
    for i in range(len(Spd)):
        if(np.isnan(Dir[i])):
            if(np.isnan(Spd[i])):
                Spd[i]=0
                Dir[i]=0
            else:
                Dir[i]=0
    return Dir,Spd


                
            

#数据去空值处理
def nan_pre(data):
    j=[]
    for indexs in data.index:
        for i in range(len(data.loc[indexs].values)):
            if(type(data.loc[indexs].values[i])==str):
                if(data.loc[indexs].values[i].find('*')!=-1):
                    j.append(indexs)
    #j=list(set(j))
    ndata=data.drop(j)
    ndata=ndata.reset_index(drop=True)
    return ndata
#数据格式转换
def info_pre(data):
    da={}
    l=data.columns.values.tolist()
    for i in l:
        dat=data[i]
        if (i!='YR--MODAHRMN'):
            dat=pd.to_numeric(dat)
        if (i=='TEMP'):
            dat=dat.astype('float')
            for j in range(len(dat)):
                dat[j]=round((dat[j]-32)/1.8,3)
        if (i=='SPD'):
            dat=dat.astype('float')
            for j in range(len(dat)):
                dat[j]=dat[j]*0.44704
        da[i]=dat
        
    ndata=pd.DataFrame(da)
    return ndata

def filePath(filename):
    path='../data/'+filename+'/'
    return path

def dataIntegration(stationname):
    toughRatio=toughness.get_toughnessratio(filePath(stationname))
    data=pd.read_excel(filePath(stationname)+'origin_dataset.xlsx')
    print('粗糙度修正系数计算完成...')
    pcp=pcp_pre(data)
    slp=slp_pre(data)
    Dir,Spd=Wind_pre(data)
    Spd=toughness.correct_toughness(toughRatio,Spd,Dir)
    other=data_pre(data,target)
    data=pd.concat([other,pcp,slp,Dir,Spd],axis=1)
    data=nan_pre(data)
    data=info_pre(data)
    data.to_excel(filePath(stationname)+'Integration_dataset.xlsx')
    print('风数据初始化完成...')
    return data

