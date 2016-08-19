import os
import asyncio
import functools

from .downloader import DownloaderYou
from .downloaderVk import DownloaderVk
from .utils_1 import utils


from concurrent.futures import ThreadPoolExecutor


class Downloader:
    def __init__(self, folder=None, config=None):
        
        self.download_folder = folder
        
        self.__downloadervk = DownloaderVk(download_folder=folder, config = config)
        self.__downloader = DownloaderYou(download_folder=folder)
        
        self.__keyWords = { "vk": self.__downloadervk,
                            "yt": self.__downloader }
        
        self.__extractorsCode = { "vk": self.__downloadervk,
                                  "youtube": self.__downloader }

    @property
    def ytdl(self):
        return self

    async def extract_info(self, loop, *args, on_error=None, retry_on_error=False, **kwargs):

        #args may contain two types of data
        #search text or 
        key = args[0].split(" ")[0]
        
        workerByUrl = self.__getWorkerByUrl(key, self.__keyWords)
        
        workerByExtractor = None
        extractor = kwargs.pop("extractor",{})
        if extractor:
            workerByExtractor = self.__getWorkerByExtractor(extractor)
        
        #check key, check url
        if key in self.__keyWords:
            argsNew = []
            argsNew.append(" ".join(args[0].split(" ")[1:]))
            result = await self.__keyWords[key].extract_info(loop, *argsNew, on_error=None, retry_on_error=False, **kwargs);
        elif workerByExtractor:
            result = await workerByExtractor.extract_info(loop, *args, on_error=None, retry_on_error=False, **kwargs);
        elif workerByUrl: 
            result = await workerByUrl.extract_info(loop, *args, on_error=None, retry_on_error=False, **kwargs);
        else:
            result = await self.__downloader.extract_info(loop, *args, **kwargs)
            
        return result


    async def safe_extract_info(self, loop, *args, **kwargs):
        
        result = await self.__downloader.extract_info(loop, *args, **kwargs)
        return result

    def prepare_filename(self, info):        
        work = self.__getWorkerByExtractor(info.get("extractor").lower())
        
        if work:
            result =  work.ytdl.prepare_filename(info)
        else: 
            result = self.__downloader.ytdl.prepare_filename(info)
    
        return result
    
    def __getWorkerByUrl(self, URL, list):
        for key,value in list.items():
            if utils.wordkWithURL(URL, value.proccedDomains):
                return value
        
    def __getWorkerByExtractor(self, extractorCode):
        for code, worker in self.__extractorsCode.items():
            if code == extractorCode:
                return worker
        