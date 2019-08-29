# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 21:50:09 2019

@author: 95722
"""

import pandas as pd
import extreme_calculate

#获取极值计算报告
def get_extremeReport(sample,label,target,filepath):
    damage_distribution=pd.DataFrame(extreme_calculate.get_number(label))
    damage_distribution.to_excel(filepath,sheet_name='damage_distribution')
    yearsample_Wspeed=[]
    allsample_Wspeed=[]
    othersample_Wspeed=[]
    typhoonsample_Wspeed=[]
    monsoonsample_Wspeed=[]
    mix_Wspeed=[]
    
    for i in range(len(target)):
        yearsample_Wspeed.append(extreme_calculate.get_gumbelextreme(sample,target[i]))
        allsample_Wspeed.append(extreme_calculate.get_paretoextreme(sample,target[i]))
        othersample_Wspeed.append(extreme_calculate.get_paretoextreme(sample,target[i],kind=0))
        typhoonsample_Wspeed.append(extreme_calculate.get_gumbelextreme(sample,target[i],kind=1))
        monsoonsample_Wspeed.append(extreme_calculate.get_paretoextreme(sample,target[i],kind=2))
        mix_Wspeed.append(extreme_calculate.get_mixextreme(sample,target[i]))
    result={}
    result['回归周期']=target
    result['年极值风速(gumbel)']=yearsample_Wspeed
    result['全样本极值风速(pareto)']=allsample_Wspeed
    result['其他类型样本极值风速(pareto)']=othersample_Wspeed
    result['台风类型样本极值风速(pareto)']=typhoonsample_Wspeed
    result['季风类型样本极值风速(pareto)']=monsoonsample_Wspeed
    result['混合分布']=mix_Wspeed
    result=pd.DataFrame(result)
    result.to_excel(filepath,sheet_name='extreme_windspeed')
    print('极值计算报告完成...')
    
def get_distributionFigure(sample,label,filepath):
    #sample=extreme_calculate.get_extremedata(sample,label)
    extreme_calculate.get_gumbelpdf(sample,filepath+'yearsample.jpg')
    extreme_calculate.get_paretopdf(sample,filepath+'allsample.jpg',ymax=1)
    extreme_calculate.get_paretopdf(sample,filepath+'othersample.jpg',kind=0,ymax=1)
    extreme_calculate.get_hist(sample,filepath+'otherhist.jpg',kind=0)
    extreme_calculate.get_gumbelpdf(sample,filepath+'typhoonsample.jpg',kind=1,ymax=1)
    extreme_calculate.get_hist(sample,filepath+'typhoonhist.jpg',kind=1)
    extreme_calculate.get_paretopdf(sample,filepath+'monsoonsample.jpg',kind=2,ymax=1)
    extreme_calculate.get_hist(sample,filepath+'monsoonhist.jpg',kind=1)
    extreme_calculate.get_mixpdf(sample,filepath+'mixedpdf.jpg',ymax=1)
    print('极值分布图完成...')


