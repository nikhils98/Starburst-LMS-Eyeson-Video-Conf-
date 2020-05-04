import os

import json
from zoomus import ZoomClient


client = ZoomClient(API_KEY, API_SECRET)

def createZoomAccount(email,name,password):

    user_info = {
        "email": email,
        "first_name": name,
        "type":1
    }
    a = client.user.create(action='create',user_info=user_info)
    print(a.content)

createZoomAccount('abc@abc.com','abc','def')

user_list_response = client.user.list()

user_list = json.loads(user_list_response.content)

for user in user_list['users']:
    user_id = user['id']
    print(json.loads(client.meeting.list(user_id=user_id).content))


