import os
from flask import Flask
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
import requests
import xmltodict
import sys
reload(sys) 
sys.setdefaultencoding('UTF8')

ar=requests.get("https://tyto.ir/quran-simple.xml")
fa=requests.get("http://tanzil.net/trans/?transID=fa.gharaati&type=xml")
en=requests.get("http://tanzil.net/trans/?transID=en.shakir&type=xml")
ar=xmltodict.parse(ar.text)
fa=xmltodict.parse(fa.text)
en=xmltodict.parse(en.text)
input=114
sure=input-1
surename=fa['quran']['sura'][sure]['@name']
d=fa['quran']['sura'][sure]['aya']
text=''
for i in range(len(d)):
 text=''
 arr=ar['quran']['sura'][sure]['aya'][i]['@text']
 enn=en['quran']['sura'][sure]['aya'][i]['@text']
 faa=fa['quran']['sura'][sure]['aya'][i]['@text']
 text='....'+str(i+1)+"...."
 text+='\n'+arr+'\n'+faa+'\n'+enn
 text+='\n'
 if len(text)<4000:
   bot.sendMessage(chat_id, text)
 else:
   bot.sendMessage(chat_id, 'too big')
 
