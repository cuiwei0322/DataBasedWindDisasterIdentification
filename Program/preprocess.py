# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:34:23 2019

@author: 95722
"""

import winddamagepiece
import dataclean
import picture
'''
可修订的参数：stationname
'''


def filePath(filename):
    path='../data/'+filename+'/'
    return path

def pre(station,limit_speed):
    dataIntegration=dataclean.dataIntegration(station)
    windpiece=winddamagepiece.piece(dataIntegration,limit_speed,station)
    picture.windpicture(windpiece,station)
    return windpiece


