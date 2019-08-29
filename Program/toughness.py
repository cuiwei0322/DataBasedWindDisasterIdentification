# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 22:56:18 2019

@author: 95722
"""

import pandas as pd
import numpy as np

'''
目的：获取[10°,360°]的粗糙度修正系数
输出格式：[(angle,toughness),(angle,toughness)]
调用参数：文件名
数据来源：'filename/tougnness.xlsx',filename是测站名
'''
filename='../data/20190116model——舟山/'   #测试文件
def get_toughnessratio(filepath):
    _origin=pd.read_excel(filepath+'toughness.xlsx')
    result=[]
    Dir=np.linspace(10,360,36).tolist()
    Ratio=[]
    #将原始数据中的点加入列表(30，60，90...)
    for i in range(len(Dir)):
        for j in range(len(_origin)):
            if(Dir[i]%360 == _origin.index[j]*30):
                result.append((int(Dir[i]),float(_origin.loc[j])/20))
                Ratio.append((int(Dir[i]),float(_origin.loc[j])/20))
    #将原始数据没有的点(10,20,40,50...)进行线性插值
    for i in range(len(Dir)):
        if(Dir[i]%30!=0):
            result.append((int(Dir[i]),float(Ratio[int(Dir[i]/30)-1][1]-(Ratio[int(Dir[i]/30)-1][1]-Ratio[int(Dir[i]/30)][1])/3*(Dir[i]%30)/10)))
    result.sort()
    _tofile=pd.DataFrame(result)
    _tofile.to_excel(filepath+'toughnessRatio.xlsx')
    return result

def correct_toughness(toughnessRatio,Spd,Dir):
    for i in range(len(Dir)):
        Spd.iloc[i]=Spd.iloc[i]*toughnessRatio[int(Dir.iloc[i]/10)-1][1]
    return Spd
tougnness = get_toughnessratio(filename)