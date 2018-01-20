import os
from flask import Flask
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
import requests
import xmltodict
import random
import time


ar=requests.get("https://tyto.ir/quran-simple.xml")
fa=requests.get("http://tanzil.net/trans/?transID=fa.gharaati&type=xml")
en=requests.get("http://tanzil.net/trans/?transID=en.shakir&type=xml")
ar=xmltodict.parse(ar.text)
fa=xmltodict.parse(fa.text)
en=xmltodict.parse(en.text)

list=[]
listnum={}
for i in range(0,114):
    surename=fa['quran']['sura'][i]['@name']
    list.append([surename])
    listnum[surename]=i
list.append(['back'])
suremarkup = ReplyKeyboardMarkup(keyboard=list ,resize_keyboard=True)
startmarkup=ReplyKeyboardMarkup(keyboard=[['list','random']] ,resize_keyboard=True)
    
    

def handle(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 if content_type == 'text':
    command = msg['text']
    print ('Got command: %s' % command)
    if command=='/start':
       bot.sendMessage(chat_id,'wellcome',reply_markup=startmarkup  )
    if command=='back':
       bot.sendMessage(chat_id,'back',reply_markup=startmarkup  )
    if command=='list':
       bot.sendMessage(chat_id,'list',reply_markup=suremarkup   )
    if command=='random':
              sure=random.randint(0,113)
              d=fa['quran']['sura'][sure]['aya']
              i=random.randint(0,len(d))
              text=''
              surename=fa['quran']['sura'][sure]['@name']
              arr=ar['quran']['sura'][sure]['aya'][i]['@text']
              enn=en['quran']['sura'][sure]['aya'][i]['@text']
              faa=fa['quran']['sura'][sure]['aya'][i]['@text']
              text='....#'+surename+'....'+str(i+1)+"...."+'\n'
              text+='\n'+arr+'\n'+enn+'\n'+faa
              text+='\n'+ str(sure+1)+":"+str(i+1)
              bot.sendMessage(chat_id,str(text))
    if command in listnum.keys():
       command=listnum[command]
       sure=int(command)
       surename=fa['quran']['sura'][sure]['@name']
       d=fa['quran']['sura'][sure]['aya']
       text=''
       for i in range(len(d)):
          text=''
          arr=ar['quran']['sura'][sure]['aya'][i]['@text']
          enn=en['quran']['sura'][sure]['aya'][i]['@text']
          faa=fa['quran']['sura'][sure]['aya'][i]['@text']
          text='....#'+surename+'....'+str(i+1)+"...."+'\n'
          text+='\n'+arr+'\n'+enn+'\n'+faa
          text+='\n'
          if len(text)<4000:
            try:
              bot.sendMessage(chat_id, text)
            except telepot.exception.TooManyRequestsError:
                time.sleep(0.5)
                try :
                  bot.sendMessage(chat_id, text)
                except telepot.exception.TooManyRequestsError:
                  time.sleep(0.5)
                  try :
                    bot.sendMessage(chat_id, text)
                  except telepot.exception.TooManyRequestsError:
                    print(str(i))
                    pass
          else:
            bot.sendMessage(chat_id, 'too big')


app = Flask(__name__)

@app.route('/')
def hello():
    return 'strix bot'

            
bot = telepot.Bot('538042986:AAFrAdw7fWN6hsm6lOSq7b8SVZzgVeJlusU')
bot.message_loop(handle)
print ('I am listening ...')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
while 1:
  time.sleep(10)
