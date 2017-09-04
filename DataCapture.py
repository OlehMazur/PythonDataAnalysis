#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: oleh
"""
import os
from ftplib import FTP, error_perm
import patoolib
import glob

def ftpDownloader(filename, host="ftp.pyclass.com", user="student@pyclass.com", passwd="student123"):
    ftp = FTP(host)
    ftp.login(user,passwd)
    ftp.cwd('Data')
    os.chdir('/home/oleh/PYDATA')
    with open(filename, 'wb') as file:
        ftp.retrbinary("RETR {}".format(filename), file.write)

def ftpDownloaderData(stationId, startYear, endYear, host="ftp.pyclass.com", user="student@pyclass.com", passwd="student123"):
    ftp=FTP(host)    
    ftp.login(user, passwd)
    if not os.path.exists('/home/oleh/PYDATA'):
        os.makedirs('/home/oleh/PYDATA')
    os.chdir('/home/oleh/PYDATA')
    for year in range(startYear, endYear+1):
        fullpath = "/Data/{}/{}-{}.gz".format(year, stationId, year)
        filename = os.path.basename(fullpath)
        try:
            with open(filename, 'wb') as file:
                ftp.retrbinary("RETR {}".format(fullpath), file.write)
            print("{} successfully downloaded".format(filename))  
        except error_perm:
            print("{} is not available".format(filename))
            os.remove(filename)
    ftp.close()
    

def extractFiles(indir='/home/oleh/PYDATA', out ='/home/oleh/PYDATA/Extracted'):
    os.chdir(indir)
    archives = glob.glob("*.gz")
    if not os.path.exists(out):
        os.makedirs(out)
    files = os.listdir("Extracted")    
    for archive in archives:
        if archive[:-3] not in files:
            patoolib.extract_archive(archive, outdir= out)
    
    
    