'''
Created on 15 авг. 2016 г.

@author: EXIA
'''
import urllib.request

class fileDownloader:

    def downloadByUrl(url):
        inputStream = urllib.request.urlopen(url)
        data = inputStream.read()
        
        return data
    
    def downloadByUrlAndSaveToFile(url,filePath):
        data = fileDownloader.downloadByUrl(url)
        
        if not data:
            return -1
        
        with open(filePath, 'wb') as file:
            file.write(data)
        
        return len(data)
    
class utils:
    def wordkWithURL(URL, domains):
        if URL.startswith("http"):
            URL = ''.join(URL.split("//")[1:])
        
        if URL.startswith("www"):
            URL = '.'.join(URL.split(".")[1:])
        
        URL = URL.split("/")[0]
        
        for i,val in enumerate(domains):
            if URL == val: return True
            
        return False
