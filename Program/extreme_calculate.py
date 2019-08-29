# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 20:52:51 2019

@author: 95722
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats

label=pd.read_excel('../data/20190116model——舟山/label.xlsx')['label'].tolist()
#修正数据格式
def get_extremedata(Data,label):
    spd=[]
    year=[]
    Dir=[]
    for i in range(len(Data)):
        index=Data[i].index[16]
        spd.append(Data[i]['SPD'][index])
        Dir.append(Data[i]['DIR'][index])
        year.append(int(Data[i]['YR--MODAHRMN'][index]/100000000))
    co_data={'spd':spd,'year':year,'label':label,'dir':Dir}
    return co_data
#获取年极值数据
def year_sample(co_data):
    result=[]
    for i in range(len(co_data['spd'])):
        if(i==0):
            year=co_data['year'][i]
            s=[]
        elif( year!=co_data['year'][i]):
            year=co_data['year'][i]
            #print(year)
            result.append(max(s))
            
            s=[]

        s.append(co_data['spd'][i])
    
    return result

#获取某风灾类型的全部样本数据
def kind_sample(co_data,label=-1):
    if(label==-1):
        result=co_data['spd']
    else:
        result=[]
        for i in range(len(co_data['spd'])):
            if(co_data['label'][i]==label):
                result.append(co_data['spd'][i])
    return result

#获取数据样本数量分布
def get_number(label):
    result=[]
    sample=list(set(label))
    for i in range(len(sample)):
        result.append(label.count(sample[i]))
    return result

#获取gumbel极值分布
def get_gumbelextreme(sample,Ryear,kind=-1):
    if(kind==-1):
        sample=year_sample(sample)
        a,b=scipy.stats.gumbel_r.fit(sample)
        rv=scipy.stats.gumbel_r(a,b)
        return rv.ppf(1.0-1/(Ryear+1))
    else:
        year=len(year_sample(sample))
        sample=kind_sample(sample,kind)
        a,b=scipy.stats.gumbel_r.fit(sample)
        rv=scipy.stats.gumbel_r(a,b)
        num=float(len(sample)/year)
        result=1.0-1/(num*(Ryear+1))
        return rv.ppf(result)

#获取pareto极值分布
def get_paretoextreme(sample,Ryear,kind=-1):
    year=len(year_sample(sample))
    sample=kind_sample(sample,kind)
    a,b,c=scipy.stats.pareto.fit(sample,floc=0)
    rv=scipy.stats.pareto(a,b,c)
    num=float(len(sample)/year)
    result=1.0-1/(num*(Ryear+1))
    return rv.ppf(result)

#获取gumbel拟合图像
def get_gumbelpdf(sample,filepath,xmin=10,xmax=50,ymin=0,ymax=0.3,kind=-1):
    if(kind==-1):
        sample=year_sample(sample)
    else:
        sample=kind_sample(sample,kind)
    a,b=scipy.stats.gumbel_r.fit(sample)
    rv=scipy.stats.gumbel_r(a,b)
    fig,ax=plt.subplots(1,1)
    ax.hist(sample,bins=range(10,45,2),normed=1,stacked=True, rwidth=0.8,histtype='stepfilled',alpha=0.4)
    x=np.linspace(xmin+2,xmax-2,1000)
    ax.plot(x,rv.pdf(x),'k-',label='gumbel_r pdf')
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.legend(loc='best')
    plt.savefig(filepath)

def get_hist(sample,filepath,kind=-1):
    if(kind==-1):
        sample=year_sample(sample)
    else:
        sample=kind_sample(sample,kind)
    fig,ax=plt.subplots(1,1)
    ax.hist(sample,bins=range(10,45,2),normed=1,stacked=True, rwidth=0.8,histtype='stepfilled',alpha=0.4)
    ax.set_ylim([0,1])
    plt.savefig(filepath)
   
def get_gumbelcdf(sample,filepath,xmin=10,xmax=50,ymin=0,ymax=1,kind=-1):
    if(kind==-1):
        sample=year_sample(sample)
    else:
        sample=kind_sample(sample,kind)
    a,b=scipy.stats.gumbel_r.fit(sample)
    rv=scipy.stats.gumbel_r(a,b)
    fig,ax=plt.subplots(1,1)
    ax.hist(sample,bins=range(15,45),normed=1,stacked=True, rwidth=0.8,histtype='stepfilled',cumulative=True,alpha=0.4)
    x=np.linspace(xmin+2,xmax-2,1000)
    ax.plot(x,rv.cdf(x),'k-',label='gumbel_r pdf')
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.legend(loc='best')
    plt.savefig(filepath)

#获取pareto拟合图像  
def get_paretopdf(sample,filepath,kind=-1,xmin=10,xmax=50,ymin=0,ymax=0.3):
    sample=kind_sample(sample,kind)
    fig,ax=plt.subplots(1,1)
    ax.hist(sample,bins=range(0,50),density=True ,stacked=True, rwidth=0.8,histtype='stepfilled',alpha=0.4)
    a,b,c=scipy.stats.pareto.fit(sample)
    rv=scipy.stats.pareto(a,b,c)
    x=np.linspace(min(sample),xmax-2,1000)
    ax.plot(x,rv.pdf(x),'k-',label='pareto pdf')
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.legend(loc='best')
    plt.savefig(filepath)

def get_paretocdf(sample,filepath,kind=-1,xmin=10,xmax=50,ymin=0,ymax=1):
    sample=kind_sample(sample,kind)
    fig,ax=plt.subplots(1,1)
    ax.hist(sample,bins=range(0,50),density=True ,stacked=True, rwidth=0.8,histtype='stepfilled',cumulative=True,alpha=0.4)
    a,b,c=scipy.stats.pareto.fit(sample)
    rv=scipy.stats.pareto(a,b,c)
    x=np.linspace(min(sample),xmax-2,1000)
    ax.plot(x,rv.cdf(x),'k-',label='pareto cdf')
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.legend(loc='best')
    plt.savefig(filepath)
    
def get_mixeddist(sample):
    S_typhoon=kind_sample(sample,1)
    S_monsoon=kind_sample(sample,2)
    S_other=kind_sample(sample,0)
    a,b=scipy.stats.gumbel_r.fit(S_typhoon)
    typhoon_dist=scipy.stats.gumbel_r(a,b)
    c,d,e=scipy.stats.pareto.fit(S_monsoon)
    monsoon_dist=scipy.stats.pareto(c,d,e)
    f,g,h=scipy.stats.pareto.fit(S_other)
    other_dist=scipy.stats.pareto(f,g,h)
    dist=[other_dist,typhoon_dist,monsoon_dist]
    weight=get_number(sample['label'])
    sumweight=sum(weight)
    for i in range(len(weight)):
        weight[i]=weight[i]/sumweight
    return dist,weight
def mix_dictcdf(dist,weight,x):
    y=0
    for i in range(len(dist)):
        y=y+weight[i]*dist[i].cdf(x)
    return y

def mix_dictpdf(dist,weight,x):
    y=0
    for i in range(len(dist)):
        y=y+weight[i]*dist[i].pdf(x)
    return y

def get_mixextreme(sample,Ryear):
    year=len(year_sample(sample))
    dist,weight=get_mixeddist(sample)
    num=float(len(kind_sample(sample))/year)
    target=1.0-1/(num*(Ryear+1))
    x=min(kind_sample(sample))
    while(1):
        if(mix_dictcdf(dist,weight,x)>target):
            return x
        else:
            x=x+0.001
            
def get_mixpdf(sample,filepath,xmin=10,xmax=50,ymin=0,ymax=1):
    dist,weight=get_mixeddist(sample)
    sample=kind_sample(sample)
    x=np.linspace(min(sample),xmax+2,1000)
    fig,ax=plt.subplots(1,1)
    ax.hist(sample,bins=range(0,50),density=True ,stacked=True, rwidth=0.8,histtype='stepfilled',alpha=0.4)
    ax.plot(x,mix_dictpdf(dist,weight,x),'k-',label='mixed pdf')
    ax.set_xlim([xmin,xmax])
    ax.set_ylim([ymin,ymax])
    ax.legend(loc='best')
    plt.savefig(filepath)