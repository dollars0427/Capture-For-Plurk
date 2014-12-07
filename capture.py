#!/usr/bin/python
# coding=UTF-8

#Import wx for create GUI interface
import wx 
#Import os for using system command
import os
#Import datatime to get current time
import datetime
#Import webbrowser to ask for authorization
import webbrowser
#Import json to encoding the string to json file
import json
#Import PlurkOauth to get token
from PlurkOauth import getRequestToken,getAccessToken
openPlurkClient = open("plurkClient","r")
plurkClient = json.loads(file.read(openPlurkClient))
requestToken,requestTokenSecret = getRequestToken(plurkClient['app_key'],plurkClient['app_secret'])

#Import imgurpython to upload the image
from imgurpython import ImgurClient
openimgurAppKey = open("imgurAppKey","r")
imgurAppkey = json.loads(file.read(openimgurAppKey))
client = ImgurClient(imgurAppkey['client_id'], imgurAppkey['client_secret'])

#Import the UI interface
import gui

#Capture screen function
current = datetime.datetime.now()

filename = "Plurk" + current.strftime("%Y-%m-%d") +".png"

catureCmd1 = "screencapture " + filename

catureCmd2 = "screencapture -i " + filename

class mainFrame(gui.mainFrame):
 
    def __init__(self, parent):
        gui.mainFrame.__init__(self, parent)
 
    def catureFullScreen(self, event):
        os.system(catureCmd1)

        if os.path.exists('imgurToken'):
            self.Show(False)
            openToken = open("imgurToken","r")
            token = json.loads(file.read(openToken))
            client.set_user_auth(token['access_token'], token['refresh_token'])
            uploadImage()

        else:
            self.Show(False)
            pinFrame(None).Show(True)

    def caturePart(self, event):
    	os.system(catureCmd2)

        if os.path.exists('imgurToken'):
            self.Show(False)
            openToken = open("imgurToken","r")
            token = json.loads(file.read(openToken))
            client.set_user_auth(token['access_token'], token['refresh_token'])
            uploadImage()

        else:
            self.Show(False)
            pinFrame(None).Show(True)

#If user do not have a access token for imgur, ask pin and get token
class pinFrame(gui.pinFrame):
 
    def __init__(self, parent):
        gui.pinFrame.__init__(self, parent)

    def getPinFromWebSite(self, event):
        auth_url = client.get_auth_url('pin')
        webbrowser.open(auth_url)

    def sendPin(self, event):
        pin = self.inputPin.GetValue()
        credentials = client.authorize(pin, 'pin')
        client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

#Save token to file
        saveToken = file('imgurToken', 'w')
        token = {"access_token":credentials['access_token'],"refresh_token":credentials['refresh_token']}

        saveToken.write(json.dumps(token))
        
        uploadImage()

        self.Show(False)
        
        PlurkPinFrame(None).Show(True)

def uploadImage():
    uploaded_image = client.upload_from_path(filename, config=None, anon=False)
    imagelink = uploaded_image['link']

#If user do not have a access token for plurk, ask pin and get token
class PlurkPinFrame(gui.PlurkPinFrame):
 
    def __init__(self, parent):
        gui.PlurkPinFrame.__init__(self, parent)

    def getPinFromWebSite(self, event):
        auth_url = 'http://www.plurk.com/OAuth/authorize?oauth_token=' + requestToken
        webbrowser.open(auth_url)

    def sendPin(self, event):
        pin = self.inputPin.GetValue()
        accessToken,accessTokenSecret = getAccessToken(plurkClient['app_key'],plurkClient['app_secret'],requestToken,requestTokenSecret,pin)

#Show Main Frame
app = wx.App(False)
mainFrame(None).Show(True)
app.MainLoop()