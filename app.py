import os
from flask import Flask
import asyncio
import telepot
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
import requests
import xmltodict
import sys
import time
import random


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
suremarkup = ReplyKeyboardMarkup(keyboard=list)
startmarkup=ReplyKeyboardMarkup(keyboard=[['list'],['random']])

class MessageCounter(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0
        
    async def on_chat_message(self, msg):
        self._command=msg['text']
        if self._command=='/start':
          self._wel='wellcome'
          await self.sender.sendMessage(self._wel,reply_markup=startmarkup )
        if self._command=='list':
          self._wel='list'
          await self.sender.sendMessage(self._wel,reply_markup=suremarkup )
        if self._command=='random':
              self._command=random.randint(0,113)
              self._d=fa['quran']['sura'][self._command]['aya']
              self._i=random.randint(0,self._d)
              self._text=''
              self._arr=ar['quran']['sura'][self._sure]['aya'][self._i]['@text']
              self._enn=en['quran']['sura'][self._sure]['aya'][self._i]['@text']
              self._faa=fa['quran']['sura'][self._sure]['aya'][self._i]['@text']
              self._text='....#'+self._surename+'....'+str(self._i+1)+"...."+'\n'
              self._text+='\n'+self._arr+'\n'+self._enn+'\n'+self._faa
              self._text+='\n'+ self._command+":"+self._i
              await self.sender.sendMessage(str(self._text))
            
        if self._command in listnum.keys():
           self._command=listnum[self._command]
           self._sure=int(self._command)
           self._surename=fa['quran']['sura'][self._sure]['@name']
           self._d=fa['quran']['sura'][self._sure]['aya']
           
           for self._i in range(len(self._d)):
              self._text=''
              self._arr=ar['quran']['sura'][self._sure]['aya'][self._i]['@text']
              self._enn=en['quran']['sura'][self._sure]['aya'][self._i]['@text']
              self._faa=fa['quran']['sura'][self._sure]['aya'][self._i]['@text']
              self._text='....#'+self._surename+'....'+str(self._i+1)+"...."+'\n'
              self._text+='\n'+self._arr+'\n'+self._enn+'\n'+self._faa
              self._text+='\n'
              if len(self._text)<4000:
                  try:
                     await self.sender.sendMessage(str(self._text))
                     
                  except telepot.exception.TelegramError as ex:
                     print(self._i)
                     time.sleep(31)
                     await self.sender.sendMessage(str(self._text))

              else:
                self._text='too big'
                print('too big')
                await self.sender.sendMessage(self._text )

app = Flask(__name__)

@app.route('/')
def hello():
    return 'strix quran'
       
            
TOKEN = '538042986:AAFrAdw7fWN6hsm6lOSq7b8SVZzgVeJlusU'  # get token from command-line
bot = telepot.aio.DelegatorBot(TOKEN, [pave_event_space()(per_chat_id(), create_open, MessageCounter, timeout=10),])
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')
loop.run_forever()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
while 1:
  time.sleep(10)
