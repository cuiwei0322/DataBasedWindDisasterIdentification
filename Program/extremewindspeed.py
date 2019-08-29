# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:55:03 2018

@author: 95722
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import pickle
import toughness

Data=pickle.load(open('../data/piece/SE19902016/584770.txt','rb'))
label=pickle.load(open('../data/label/testmodel20181023/train.txt','rb'))[1]
spd=[]
year=[]
Dir=[]
ratio=toughness.get_toughnessratio('../data/20190116model——舟山/')
for i in range(len(Data)):
    index=Data[i].index[16]
    spd.append(Data[i]['SPD'][index])
    Dir.append(Data[i]['DIR'][index])
    year.append(int(Data[i]['YR--MODAHRMN'][index]/100000000))

for i in range(len(spd)):
    for j in range(len(ratio)):
        if(Dir[i]==ratio[j][0]):
            spd[i]=spd[i]*ratio[j][1]
            break

data={'spd':spd,'year':year,'label':label,'dir':Dir}
def gumbel_pdf(x, mu=0, beta=1):
    z = (x - mu) / beta
    return np.exp(-z - np.exp(-z)) / beta

def year_sample(data):
    result=[]
    for i in range(len(data['spd'])):
        if(i==0):
            year=data['year'][i]
            s=[]
        elif( year!=data['year'][i]):
            year=data['year'][i]
            result.append(max(s))
            
            s=[]
        else:
            s.append(data['spd'][i])
    
    return result

def year_speed(sample,num=50):
    mean=np.mean(sample)
    std=np.std(sample)
    beta=std*np.sqrt(6)/np.pi
    u=mean-0.45005*std
    result=u-beta*np.log(np.log(num/(num-1)))
    return result
def p_extreme(year,spd):
    num=float(len(spd)/26)
    print(num)
    result=1.0-1/(num*(year+1))
    print(result)
    return result
def kind_sample(data,label):
    result=[]
    for i in range(len(data['spd'])):
        if(data['label'][i]==label):
            result.append(data['spd'][i])
    return result
year_data=np.array(year_sample(data))
year_data.sort()

a,b=scipy.stats.gumbel_r.fit(year_data)
rv=scipy.stats.gumbel_r(a,b)
print(rv.ppf(1.0-1/101))

fig,ax=plt.subplots(1,1)
ax.hist(year_data,bins=range(15,45),normed=1,stacked=True, rwidth=0.8,histtype='stepfilled',cumulative=True,alpha=0.4)
x=np.linspace(15,50,1000)
ax.plot(x,rv.cdf(x),'k-',label='gumbel_r pdf')
ax.set_xlim([10,50])
ax.legend(loc='best')

fig.show()   
#spd=kind_sample(data,0)
#spd.sort()
#spd_min=spd[0]
fig,ax=plt.subplots(1,1)
ax.hist(spd,bins=range(0,50),density=True ,stacked=True, rwidth=0.8,histtype='stepfilled',cumulative=True,alpha=0.4)

a,b,c=scipy.stats.pareto.fit(spd)

print(min(spd))
rv=scipy.stats.pareto(a,b,c)
x=np.linspace(0.00,50,1000)
ax.plot(x,rv.cdf(x),'k-',label='pareto pdf')
#ax.set_xlim([14,50])
#ax.set_ylim([0,0.3])
print(rv.ppf(p_extreme(50,spd)))