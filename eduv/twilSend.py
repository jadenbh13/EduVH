import random
import time
from twilio.rest import Client

account_sid = "AUTH_SID"
auth_token  = "AUTH_Token"
client = Client(account_sid, auth_token)
#Authenticate twilio account with SID and token

def sendMess(msg, numb):
    message = client.messages \
                    .create(
                         body=msg,
                         from_='+12059842903',
                         to=numb
                     )
    #Create new message with args given
    print(message.sid)
    #Print SID to confirm sending
