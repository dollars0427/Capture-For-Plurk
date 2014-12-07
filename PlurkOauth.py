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
#Import json to encoding the string to json file
import json

def getRequestToken(appKey,appSecret):
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

	requestTokenSecret = requestTokenQs['oauth_token_secret'][0]

	return requestToken,requestTokenSecret

def getAccessToken(appKey,appSecret,requestToken,requestTokenSecret,pin):
	url = 'http://www.plurk.com/OAuth/access_token'

	params = {
    	'oauth_version': "1.0",
    	'oauth_nonce': oauth.generate_nonce(),
    	'oauth_timestamp': int(time.time()),
    	'oauth_verifier':pin
	}

	consumer = oauth.Consumer(key= appKey, secret= appSecret)
	token = oauth.Token(key=requestToken, secret=requestTokenSecret)

	params['oauth_consumer_key'] = consumer.key
	params['oauth_token'] = token.key

	req = oauth.Request(method="GET", url=url, parameters=params)

	signature_method = oauth.SignatureMethod_HMAC_SHA1()

	req.sign_request(signature_method, consumer,token)

	getAccessToken = requests.get(url,params = req)

	accessTokenQs = urlparse.parse_qs(getAccessToken.text)

	accessToken = accessTokenQs['oauth_token'][0]

	accessTokenSecret = accessTokenQs['oauth_token_secret'][0]

	saveToken = file('plurkToken', 'w')

	token = {"access_token":accessToken,"access_token_secret":accessTokenSecret}

	saveToken.write(json.dumps(token))

	return accessToken,accessTokenSecret

def addPlurk(appKey,appSecret,accessToken,accessTokenSecret,content):
	url = 'http://www.plurk.com/APP/Timeline/plurkAdd'

	params = {
    	'oauth_version': "1.0",
    	'oauth_nonce': oauth.generate_nonce(),
    	'oauth_timestamp': int(time.time())
	}

	consumer = oauth.Consumer(key= appKey, secret= appSecret)
	token = oauth.Token(key=accessToken, secret=accessTokenSecret)

	params['oauth_consumer_key'] = consumer.key
	params['oauth_token'] = token.key
	params['content'] = content.encode('utf-8')
	params['qualifier'] = 'says'
	params['no_comments'] = 0

	req = oauth.Request(method="GET", url=url, parameters=params)

	signature_method = oauth.SignatureMethod_HMAC_SHA1()

	req.sign_request(signature_method, consumer,token)

	postPlurk = requests.get(url,params = req)
