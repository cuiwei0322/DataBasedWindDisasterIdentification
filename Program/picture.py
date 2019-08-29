# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 15:55:08 2018

@author: 95722
"""

import pickle
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


test=pickle.load(open('../data/piece/SE19902016/588470.txt','rb'))
#test=test[1:3]
matplotlib.use('Agg')
def create(num):
    a=[]
    for i in range(1,num):
        a.append(num+1)
    return a
def zuobiao(x1,y1,size=7,derx=0.1,dery=0.3):
    for a, b in zip(x1, y1):  
        plt.text(a+derx, round(b,2)+dery, round(b,2),ha='center', va='bottom', fontsize=size)  

def get_data(data,i):
    test_1=data[i]
    Spd=list(test_1['SPD'])
    Dir=list(test_1['DIR'])
    Temp=list(test_1['TEMP'])
#    Dewp=list((test_1['DEWP']-32)/1.8)
    Slp=list(test_1['SLP'])
    pcp=list(test_1['PCP06'])
    time=list(test_1['YR--MODAHRMN'])
    index=np.linspace(1,33,33).tolist()
    ndata=[index,Spd,Dir,Slp,pcp,Temp,time]
    return ndata
def square(start,end):
    plt.plot((start[0],end[0]),(start[1],start[1]),color='black') #1
    plt.plot((start[0],start[0]),(end[1],start[1]),color='black') #2
    plt.plot((start[0],end[0]),(end[1],end[1]),color='black') #3
    plt.plot((end[0],end[0]),(end[1],start[1]),color='black') #4

'''
data格式：
    1. index 索引
    2. Spd   风速
    3. Dir   风向
    4. Slp   大气压
    5. pcp   降水
    6. Temp  大气温度
    7. Dewp  露点温度
    8. time  时间
'''
def draw_picture(data,result):
    #设置画布大小
    plt.figure(figsize=(20,15))
    xtick=np.linspace(1,33,33)
    date=data[6][int((len(data[6])-1)/2)]
    
    #绘制1号——速度时序折线图
    plt.subplot(321)
    plt.ylabel(r'wind speed(m/s)')
    plt.plot(data[0],data[1],'r--')
    plt.xticks(xtick)
    plt.ylim((0,35))
    zuobiao(data[0],data[1])
#    
#    #绘制2号——风速时序散点图
    plt.subplot(322)
    plt.scatter(data[0],data[2],marker='o',color='blue',s=10)
    plt.ylabel('Dir(°)')
    plt.xticks(xtick)
    plt.yticks(np.linspace(0,360,7))
    zuobiao(data[0],data[2])
#    
#    #绘制3号——气压时序折线图
    plt.subplot(323)
    plt.ylabel('atmospheric pressure(0.1kpa)')
    plt.plot(data[0],data[3],'r--',color='green')
    plt.xticks(xtick)
    plt.ylim((980,1050))
    plt.yticks([980,990,1000,1010,1020,1030,1040,1050,1013.25],['980','990','1000','1010','1020','1030','1040','1050',r'$Standard$'])
    zuobiao(data[0],data[3])
#    
#    #绘制4号——降水时序折线图
    plt.subplot(324)
    plt.ylabel('3-hour precipitation(mm)')
    plt.plot(data[0],data[4],'r--',color='blue')
    plt.xticks(xtick)
    plt.ylim((0,40))
    zuobiao(data[0],data[4],7,0.1,0.01)
#    
#    #绘制5号——温度时序折线图
    plt.subplot(313)
    plt.ylabel('temperature(℃)')
    l1, = plt.plot(data[0],data[5],'r-o',color='red')
    zuobiao(data[0],data[5])
    plt.xticks(xtick)
    plt.ylim((-10,40))
    
    l2, = plt.plot(data[0],data[6],'r--',color='blue')
    zuobiao(data[0],data[6])
    plt.xticks(xtick)
    plt.legend(handles=[l1,l2,],labels=['temp','dewp'],loc='best')
    
    plt.suptitle(r'$%s$'%date,fontsize=16,)
    plt.savefig(result+'%s.jpg'%date)
    plt.close()
    print('%s ... done'%date)
    
    return date
def filePath(filename):
    path='../data/'+filename+'/'
    return path

def windpicture(data,stationname):
    Id=[]
    t=[]
    if(os.path.exists(filePath(stationname)+'Picture')==0):
        os.mkdir(filePath(stationname)+'Picture')
        for i in range(len(data)):
            d=get_data(data,i)        
            time=draw_picture(d,filePath(stationname)+'Picture/')
            Id.append(i)
            t.append(time)
        #label=pd.DataFrame({'id':Id,'time':t})
        #label.to_excel(filePath(stationname)+'label.xlsx')
        print('切片数据绘图完成...')
    else:
        print('跳过数据绘图...')