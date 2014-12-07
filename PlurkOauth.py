#!/usr/bin/python
#coding=UTF-8

#Import oauth to ask for token
import oauth2 as oauth
#Import webbrowser to ask for authorization
import webbrowser
#Import time to get current time
import time
#Import requests to send request to plurk
import requests
#Import urlparse to parse the response
import urlparse 

def getAccessToken(appKey,appSecret):
	url = 'http://www.plurk.com/OAuth/request_token'

	params = {
    	'oauth_version': "1.0",
    	'oauth_nonce': oauth.generate_nonce(),
    	'oauth_timestamp': int(time.time())
	}

	consumer = oauth.Consumer(key= appKey, secret= appSecret)

	params['oauth_consumer_key'] = consumer.key

	req = oauth.Request(method="GET", url=url, parameters=params)

	signature_method = oauth.SignatureMethod_HMAC_SHA1()

	req.sign_request(signature_method, consumer,None)

	getrequestToken = requests.get(url,params = req)

	requestTokenQs = urlparse.parse_qs(getrequestToken.text)

	requestToken = requestTokenQs['oauth_token'][0]

	authUrl = 'http://www.plurk.com/OAuth/authorize?oauth_token=' + requestToken

	webbrowser.open(authUrl)