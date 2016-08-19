import os
import asyncio
import functools
import youtube_dl
from .vkApi_impl import vkReq
from concurrent.futures import ThreadPoolExecutor
from vk.exceptions import VkAPIError
from . utils_1 import fileDownloader


class DownloaderVk:
    
    proccedDomains = { "vk.com", "vkontakte.com" }
        

    def __init__(self, download_folder = None, config = None):
        self.vkapiConfig = { "token":config.Vktoken, "username":config.Vkuser, "password":config.Vkpassword, "vkAppid":config.VkAppid}
        
        if not self.vkapiConfig.get("token") and not (self.vkapiConfig.get("username") and self.vkapiConfig.get("password") and self.vkapiConfig.get("vkAppid")):
            raise Exception("to work with vk specify Vktoken or VkAppid, Vkuser, Vkpassword in options.ini")
        
        self.vkApi = vkReq( self.vkapiConfig )
        self.checkConnection()
        
        #request params
        self.auto_complete = 1
        self.searchCount = 1
        
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        self.download_folder = download_folder

    def checkConnection(self):
        try:
            responce = self.vkApi.checkCoonnectionWork()
        except VkAPIError as e:
            print("Token correct: %s" % e.is_access_token_incorrect())
            print("Captcha Need: %s" % e.is_captcha_needed())
            print("Reqs params %s" % VkAPIError.get_pretty_request_params(e.error_data))
            print("Error Code: %s \nError Message: %s" % (e.code, e.message))
            print("Check token!")
            print("\n")
            
    @property
    def ytdl(self):
        return self

    async def extract_info(self, loop, *args, on_error=None, retry_on_error=False, **kwargs):
        
        responce = None
        
        responce = self.__audioGetById(' '.join(args))

        if not responce:
            responce = self.__audioSearch(' '.join(args))
   
        if not responce:
            return None
        
        responce = self.reconstructResponce(responce)      
        
        if kwargs.get("download"):
            urlStrip = responce["url"].split("?")[0]
            
            print("[Download] Started:", urlStrip)
            
            result = fileDownloader.downloadByUrlAndSaveToFile(responce["url"], self.__constructFilenameFromUrl(responce["url"]))
            if result < 0:
                return None
            
            print("[Download] Complete:", urlStrip)
            
        return responce
    
    #for support interface    
    async def safe_extract_info(self, loop, *args, **kwargs):
        return await extract_info(self, loop, *args, **kwargs)

    def reconstructResponce(self, list):
        reconstructResponce = {}

        reconstructResponce["extractor"] = "vk"
        reconstructResponce["url"] = list[0]["url"]
        reconstructResponce["uploader_id"] = list[0]["owner_id"]
        reconstructResponce["webpage_url"] = str(list[0]["owner_id"]) + "_" + str(list[0]["id"])
        reconstructResponce["title"] = list[0]["title"]
        reconstructResponce["duration"] = list[0]["duration"]

        return reconstructResponce
    
    def prepare_filename(self, info):
        return self.__constructFilenameFromUrl(info["url"])
    
    def __constructFilenameFromUrl(self, info):
        path = os.path.join(self.download_folder, info.split("?")[0].split("/")[-1])
        
        return path
    
    def __audioSearch(self, req):
        responce = None
        responce = self.vkApi.sendRequest("audio.search", auto_complete = self.auto_complete, count = self.searchCount, q = req)
            
        if not responce or len(responce.get("items")) <= 0:
                return None
            
        return responce["items"]
    
    def __audioGetById(self, req):
        responce = None
        try:
            responce = self.vkApi.sendRequest("audio.getById", audios = req)
            
            if len(responce) <= 0:
                return None
            
        except Exception:
            return None
        
        return responce
                        
                        
                        
                        
                        
                        
                        
                        