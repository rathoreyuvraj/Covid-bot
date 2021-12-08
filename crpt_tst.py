from BOTTEL import telegram_chatbot
import json
import numpy as np
import requests
import ast
from datetime import datetime
from urllib.request import urlopen
# loads subscriber data
with open("SubData.txt", "r+") as withRp:
    cont = withRp.read()
if cont != "":
    ub = ast.literal_eval(cont)
else:
    ub = {}

with open("ud.txt", "r+") as withRp:
    cont = withRp.read()
if cont != "":
    list = ast.literal_eval(cont)
else:
    list = {}
print(list)
st=-100000000;sth=100000000;portfol=66;inv=2900
bot = telegram_chatbot("config.cfg")
# this adds subscriber
def checker(list):
   #try:
    response = requests.get("https://api.wazirx.com/api/v2/tickers")
    obj = response.json()

    for it,dat in list.items():
     ik=it+"inr"
     pr = float(obj[ik]["last"])
     prt=pr*float(dat[2])
     st=float(dat[0]);sth=float(dat[1])
     #print(it+" "+str(dat))
     pr = (obj[ik]["last"])
     delt = prt - float(dat[3])
     if(prt<st or prt>sth ):
        # print(st)
        # print(sth)
        if(delt<0):
            txts="FALLING\n"
        else:
            txts="PROFIT\n"
        bot.send_message(txts+"ALERT\n"+it.upper()+" "+str(pr)+"\n"+"\nDelta "+str(int(delt))+"\nPORTFOLIO= "+str(int(prt))+"\n",650222726)
   #except:
       #print("FAIL")
def SubTimer(msg, id):
    if informer(msg) != "Please enter correct district. You may check spelling on Google :)":
        ub[id] = msg
        with open("SubData.txt", "r+") as withRp:
            withRp.truncate()
            withRp.write(str(ub))
        return "You Are Now Subscribed.\nYou will recieve daily Corona Updates at 9 am everyday." + "\n\n" + informer(
            msg)
    else:
        return "Press /daily again and re-Enter Correct District spelling"
# this is schedule message sender
def sender():
    print("Schedule Message Sent")
    for ids, dists in ub.items():
        bot.send_message("Good Morning\n\n"+str(informer(dists)), ids)


# this is main function which uses json data from covid 19 api and searches it "
def informer(dist):
   print("inf")
   m="";tsd=0

   try:
    response = requests.get("https://api.wazirx.com/api/v2/tickers")
    obj = response.json()
    for it,dat in list.items():
     ik=it+"inr"
     pr = float(obj[ik]["last"])
     prt=pr*float(dat[2])
     st=float(dat[0]);sth=float(dat[1])
     #print(it+" "+str(dat))
     #m=str(str(pr)+"\n"+"PORTFOLIO= "+str(prt)+"\n"+it.upper(),650222726)
     pr=(obj[ik]["last"])
     delt=prt-float(dat[3])
     tsd+=delt
     #print("her")
     m+=str("\n"+it.upper()+"\n"+"Price "+pr+"\nDelta "+str(int(delt))+"\nPortfolio "+str(int(prt))+"\n")
    return m+"\nTotal Delta "+str(int(tsd))
   except Exception as exed:
       return exed



print("Bot server is ON")
# this processes the input
def make_reply(msg):
    reply = None
    if msg is not None:
        reply = informer(msg)
        print(msg)
        return reply
# id for knowing if subbscribe request
stid = False
update_id = None
# this lop fetch updates and passes it
while True:
    message=checker(list)
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]  # this stors all user id text etc

    # below lines checks if updates have came or timeout is done(came is +1 update id)
    # if came it fetch message text and user id . it sends meesage INPUT to the make reply function ,the OUTPUT
    # from this make reply is returned to send message function with user id that this fetched from updates
    # takes input and SUBSCRIBER ID and sends ,this message reciever
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
                print(message)
            except:
                message = None
            from_ = item["message"]["from"]["id"]  # id
            try:
                print(item["message"]["from"]["username"])
            except:
                print(str(item["message"]["from"]["first_name"])+" "+str(item["message"]["from"]["last_name"]))
            if message == "/daily":
                print(message)
                bot.send_message("Enter District for which you would like daily updates", from_)
                stid = True
            elif stid is True:
                stid = False
                reply = SubTimer(message, from_)  # sent to process input
                print(message + " >>" + "sucess subs")
                bot.send_message(reply, from_)  # returns output with  id
            elif "Setl" in message:
                print(message)
                try:
                 st=float(message[4:])
                except:
                  None
            elif "Seth" in message:
                print(message)
                try:
                 sth = float(message[4:])
                except:
                  None
            elif "inv" in message.lower():
                print("ds")
                inv=float(message[4:])
            elif "stats" in message.lower():
                stry=str(list)
                bot.send_message(stry,from_)
            elif "rem" in message.lower():
                m = message
                tar = m.split()
                del list[tar[1]]
                bot.send_message(list,from_)
            elif "add" in message.lower():
                m=message
                tar=m.split()
                try:
                    list[tar[1]]=[tar[2],tar[3],tar[4],tar[5]]
                    bot.send_message(list,from_)
                except:
                    bot.send_message("REENTER",from_)
            elif "mod" in message.lower():
                m=message
                tar=m.split()
                try:
                    if len(tar)==5:
                        print(list[tar[1]])

                        list[tar[1]] = [tar[2], tar[3], tar[4],list[tar[1]][3]]
                    elif len(tar)>2:

                     val=int(tar[2])
                     list[tar[1]][val] = float(tar[3])


                    elif (tar[1] in list):
                       list[tar[1]] =[-1000000,10000000,list[tar[1]][2],list[tar[1]][3]]
                    else:
                         list[tar[1]] = [0, 0, 0, 0]



                    bot.send_message(list,from_)
                except Exception as tts:
                       bot.send_message(tts,from_)
            elif "mon" in message.lower():
                m = message
                tar = m.split()

                try:
                 list[tar[1]][0] = float(tar[2]) * float(list[tar[1]][2])
                 list[tar[1]][1] = float(tar[3])*float(list[tar[1]][2])
                except:
                  bot.send_message("inld",from_)
                bot.send_message(list,from_)
            elif "dict" in message.lower():
                list={}
                list=ast.literal_eval(message[5:])
            else:
                reply = make_reply(message)
                bot.send_message(reply, from_)
