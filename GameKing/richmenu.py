import os
import requests

def switchTo(userId, richmenuId):
    headers = {
        "Authorization":"Bearer " + os.environ['Channel_access_token'], "Content-Type":"application/json"
    }
    req = requests.request('POST', 'https://api.line.me/v2/bot/user/' + userId + '/richmenu/' + richmenuId, 
                           headers=headers)
    return req.text
