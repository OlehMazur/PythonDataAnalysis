#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 14:50:25 2017

@author: oleh
"""

import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns

def addField(indir='/home/oleh/PYDATA/Extracted'):
    os.chdir(indir)
    fileList = glob.glob("*")
    for filename in fileList:
        df = pd.read_csv(filename, sep='\s+', header=None)
        df["Station"] = [filename.rsplit("-",1)[0]]*df.shape[0]
        df.to_csv(filename + '.csv', index=None, header=None)
        
def concatenate(indir='/home/oleh/PYDATA/Extracted', outfile= '/home/oleh/PYDATA/OUT/Concatenated.csv'):
    os.chdir(indir)
    fileList = glob.glob("*.csv")
    dfList=[]
    colnames= ["Year", "Month", "Day", "Hour", "Temp", "DewTemp","Pressure", "WindDir", "WindSpeed", "Sky","Precip1","Precip6", "ID"]
    for filename in fileList:
        print(filename)
        df = pd.read_csv(filename, header=None)
        dfList.append(df)
    concatDf = pd.concat(dfList, axis=0)
    concatDf.columns = colnames
    concatDf.to_csv(outfile, index=None)
  
    
def merge(left='/home/oleh/PYDATA/OUT/Concatenated.csv', right='/home/oleh/PYDATA/OUT/station-info.txt', output='/home/oleh/PYDATA/OUT/Concatenated-Merged.csv'):
    leftDf = pd.read_csv(left)
    rightDf = pd.read_fwf(right, converters={"USAF":str,"WBAN":str})
    rightDf["USAF_WBAN"] = rightDf["USAF"] +"-"+rightDf["WBAN"]
    mergeDf = pd.merge(leftDf, rightDf.loc[:,["USAF_WBAN", "STATION NAME","LAT","LON"]], left_on="ID", right_on="USAF_WBAN")
    mergeDf.to_csv(output)
    

def pivot(infile='/home/oleh/PYDATA/OUT/Concatenated-Merged.csv', outfile='/home/oleh/PYDATA/OUT/Pivoted.csv'):
    df = pd.read_csv(infile)  
    df = df.replace(-9999, np.nan)
    df["Temp"] = df["Temp"]/10.0
    table = pd.pivot_table(df, index=["ID"], columns="Year", values="Temp")
    table.to_csv(outfile)
    return table
    

def plot(outfigure= '/home/oleh/PYDATA/OUT/Ploted.png'):
    df = pivot()
    df.T.plot(subplots=True, kind='bar')
    sns.plt.savefig(outfigure, dpi=200)