import os
from flask import Flask
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import requests
import xmltodict
import sys
import time
#reload(sys) 
#sys.setdefaultencoding('UTF8')

ar=requests.get("https://tyto.ir/quran-simple.xml")
fa=requests.get("http://tanzil.net/trans/?transID=fa.gharaati&type=xml")
en=requests.get("http://tanzil.net/trans/?transID=en.shakir&type=xml")
ar=xmltodict.parse(ar.text)
fa=xmltodict.parse(fa.text)
en=xmltodict.parse(en.text)



app = Flask(__name__)

@app.route('/')
def hello():
    return 'strix bot'

def handle(msg):
 content_type, chat_type, chat_id = telepot.glance(msg)
 if content_type == 'text':
    command = msg['text']
    print ('Got command: %s' % command)
    sure=int(command)-1
    surename=fa['quran']['sura'][sure]['@name']
    d=fa['quran']['sura'][sure]['aya']
    text=''
    for i in range(len(d)):
       text=''
       if i in range(0,280,1):
          time.sleep(0.5)  
       arr=ar['quran']['sura'][sure]['aya'][i]['@text']
       enn=en['quran']['sura'][sure]['aya'][i]['@text']
       faa=fa['quran']['sura'][sure]['aya'][i]['@text']
       text='....#'+surename+'....'+str(i+1)+"...."+'\n'
       text+='\n'+arr+'\n'+enn+'\n'+faa
       text+='\n'
       if len(text)<4000:
         bot.sendMessage(chat_id, text)
       else:
         bot.sendMessage(chat_id, 'too big')
bot = telepot.Bot('538042986:AAFrAdw7fWN6hsm6lOSq7b8SVZzgVeJlusU')
bot.message_loop(handle)
print ('I am listening ...')

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
while 1:
  time.sleep(10)
