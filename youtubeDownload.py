#!/usr/bin/env python

from __future__ import unicode_literals
import os
import sys
sys.path.append('../youtube-dl')
import youtube_dl
import pandas as pd

class Downloader:
    def __init__(self, isMp3 = False, downloadDirectory =  "./downloadlarim", saveFile = 'downloadedList.csv' ):
        self.isMp3 = False
        self.saveFile = saveFile
        self.downloadDirectory =downloadDirectory

    def setMp3(self,a):
        self.isMp3 = a
    def setDownloadDir(self,d):
        self.downloadDirectory = d
    def setSaveFile(self, s):
        self.saveFile = s

    def goToDir(self, directory):
        import os
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir(directory)

    def getOpts(self, isMp3):
        ydl_opts = {"ytsearch":"h"}
        if(isMp3):
            ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

        return ydl_opts

    def getToDownloadId(self, a, f):
        try:
            df = pd.read_csv(f)
        except:
            df = pd.DataFrame({'uploader' : [],'title' : [],'date': [],'url':[],'id':[]})
            df.to_csv(f)

        b = a['entries']
        out = {"downloadList":[],"titles":[],"dates":[],"uploader":[],'id':[]}
        for i in b:
            pass
            if(not ((df['id'] == i['id'])).any()):
                out["downloadList"].append(i['webpage_url'])
                out["titles"].append(i['title'])
                out["dates"].append(i['upload_date'])
                out["uploader"].append(i['uploader'])
                out['id'].append(i['id'])
        return out

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def updateDownloadedList(self, out, f):

        try:
            a = pd.read_csv(f)
        except:
            a = pd.DataFrame({'uploader' : [],'title' : [],
     'date': [],'url':[],'id':[]
      })

        df = pd.DataFrame({'uploader' : out['uploader'],'title' : out['titles'],
     'date': out['dates'],'url':out['downloadList'],'id':out['id']
      })
        df = df.append(a)
        df.to_csv(f, mode = 'w', index = False, encoding='utf-8')


    def downloadList(self, url):

        ydl_opts = self.getOpts(self.isMp3)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            a = ydl.extract_info(url,download = False)
            out = self.getToDownloadId(a,self.saveFile)
            self.updateDownloadedList(out,self.saveFile)

            self.downloadDirectory = a['title']
            self.goToDir(self.downloadDirectory)
            ydl.download(out['downloadList'])


