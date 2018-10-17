from gsearch import *
from gsearch.googlesearch import search
import wikipedia
from google_images_download import google_images_download
import urbandict
import logger
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

GLOBAL_LIMIT = 9
# TG API limit. An album can have atmost 10 media!
TMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./../DOWNLOADS/")


def progress(current, total):
    print("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@bot.on(events.NewMessage(pattern=r"\.google (.*)"))
@bot.on(events.MessageEdited(pattern=r"\.google (.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1) # + " -inurl:(htm|html|php|pls|txt) intitle:index.of \"last modified\" (mkv|mp4|avi|epub|pdf|mp3)"
    search_results = search(input_str, num_results=GLOBAL_LIMIT)
    output_str = " "
    for text, url in search_results:
        output_str += "  🔎 [{}]({}) \n\n".format(text, url)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds. \n{}".format(input_str, ms, output_str), link_preview=False)

@bot.on(events.NewMessage(outgoing=True, pattern=".img (.*)"))
@bot.on(events.MessageEdited(outgoing=True, pattern=".img (.*)"))
async def img_sampler(e):
 await e.edit('Processing...')
 start=round(time.time() * 1000)
 s = e.pattern_match.group(1)
 lim = re.findall(r"lim=\d+", s)
 try:
  lim = lim[0]
  lim = lim.replace('lim=', '')
  s = s.replace('lim='+lim[0], '')
 except IndexError:
  lim = 2
 response = google_images_download.googleimagesdownload()
 arguments = {"keywords":s,"limit":lim, "format":"jpg"}   #creating list of arguments
 paths = response.download(arguments)   #passing the arguments to the function
 lst = paths[s]
 await bot.send_file(await bot.get_input_entity(e.chat_id), lst)
 end=round(time.time() * 1000)
 msstartend=int(end) - int(start)
 await e.edit("Done. Time taken: "+str(msstartend) + 's')
@bot.on(events.NewMessage(outgoing=True,pattern=r'.wiki (.*)'))
@bot.on(events.MessageEdited(outgoing=True,pattern=r'.wiki (.*)'))
async def wiki(e):
        match = e.pattern_match.group(1)
        result=wikipedia.summary(match)
        await bot.send_message(await bot.get_input_entity(e.chat_id), message='**Search:**\n`' + match + '`\n\n**Result:**\n' + result, reply_to=e.id, link_preview=False)
        if LOGGER:
           await bot.send_message(LOGGER_GROUP,"Wiki query "+match+" was executed successfully")
@bot.on(events.NewMessage(outgoing=True, pattern='^.ud (.*)'))
@bot.on(events.MessageEdited(outgoing=True, pattern='^.ud (.*)'))
async def ud(e):
  await e.edit("Processing...")
  str = e.pattern_match.group(1)
  mean = urbandict.define(str)
  if len(mean) >= 0:
    await e.edit('Text: **'+str+'**\n\nMeaning: **'+mean[0]['def']+'**\n\n'+'Example: \n__'+mean[0]['example']+'__')
    if LOGGER:
        await bot.send_message(LOGGER_GROUP,"ud query "+str+" executed successfully.")
  else:
    await e.edit("No result found for **"+str+"**")




    ######TTS AND TRT will be back soon :/
    ######Need to implement a new api


#EXTRA......... WHAT IS

page = requests.get('http://google.com/search?q=define+api') 
soup = BeautifulSoup(page.text, 'html.parser') 
print (soup.find(class_='PNlCoe XpoqFe'))
# html = open('test.html', 'w') html.write(str(soup))





@bot.on(events.NewMessage(pattern='^.whatis (.*)')) 
async def whatis(e):
	s = e.pattern_match.group(1)
	page = requests.get('http://google.com/search?q='+s)
	soup = BeautifulSoup(page.text, 'html.parser')
	print(soup.find(class_='mrH1y'))
