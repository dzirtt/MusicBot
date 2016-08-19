'''
Created on 15 авг. 2016 г.

@author: EXIA


param:
    string token
    string appid, username, password
    string vkApiVersion

'''

import vk
from vk.exceptions import VkAPIError


class vkReq:
    def __init__(self, params):
        self.params = params
        
        if self.params.get('token'):       
            vkSession = vk.Session(access_token = self.params['token'])
        elif self.params.get('username') and self.params.get('password') and self.params.get('appid'):
            vkSession = vk.AuthSession(app_id = self.params['appid'], user_login = self.params['username'], user_password = self.params['password'])
            
        self.vkApi = vk.API(vkSession, v=self.params.get('vkApiVersion','5.35'), lang='ru', timeout=10)
    
    def checkCoonnectionWork(self):
        if not self.vkApi: 
            return False
        
        try:
            response = self.vkApi.getServerTime()
        except VkAPIError as e:
            raise e 
             
        if response:
            return True
        else:
            return False
        
    
    def sendRequest(self, method, **params):
        return getattr(self.vkApi, method)(**params)