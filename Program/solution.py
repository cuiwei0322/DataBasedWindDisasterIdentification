# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 23:14:06 2019

@author: 95722
"""

import preprocess
import afterprocess
import pandas as pd
import extreme_calculate
import os
'''
参数集：
    stationname：测站名
    limit_speed：限速
    target:回归年份
    label:label表格,csv格式
    analyze_path：分析结果文件路径
    reportpath：极值风速报告路径
    
'''
stationname='20190210model——嵊州'
limit_speed=12
target=[1,2,3,4,5,10,25,50,100,700]

analyze_path='../data/'+stationname+'/analyze/'
#label=pd.read_excel('../data/%s/label.xlsx'%stationname)['label'].tolist()
os.mkdir(analyze_path)
reportpath=analyze_path+'Report.xlsx'

'''
'''

#winddata=preprocess.pre(stationname,limit_speed)
#sample=extreme_calculate.get_extremedata(winddata,label)
#afterprocess.get_extremeReport(sample,label,target,reportpath)
#afterprocess.get_distributionFigure(sample,label,analyze_path)
