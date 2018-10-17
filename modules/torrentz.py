# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import requests
from datetime import datetime
import cfscrape # https://github.com/Anorov/cloudflare-scrape
from bs4 import BeautifulSoup
import urllib.parse


@bot.on(events.NewMessage(pattern=r".torrentz (torrentz2\.eu|idop\.se) (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_type = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    search_results = []
    if input_type == "torrentz2.eu":
        search_results = Scrapper.SearchTorrentz(input_str)
    elif input_type == "idop.se":
        search_results = Scrapper.SearchIdopeSe(input_str)
    output_str = ""
    i = 0
    for result in search_results:
        if i > 5:
            break
        url = "`" + result["hash"] + "`"
        message_text = " 👉🏻 " + result["title"] + ": " + url + " \r\n"
        message_text += " FILE SIZE: " + result["size"] + "\r\n"
        # message_text += " Uploaded " + result["date"] + "\r\n"
        message_text += " SEEDS: " + result["seeds"] + " PEERS: " + result["peers"] + " \r\n"
        message_text += "===\r\n"
        output_str += message_text
        i = i + 1
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Scrapped {} for {} in {} seconds. Obtained Results: \n {}".format(input_type, input_str, ms, output_str))


@bot.on(events.NewMessage(pattern=r".torrentz hash (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    magnetic_link = Scrapper.GetMagneticLink(input_str)
    end = datetime.now()
    ms = (end - start).seconds
    output_str = "Obtained Magnetic Link `{}` for the Info Hash: {} in {} seconds.".format(magnetic_link, input_str, ms)
    await event.edit(output_str)


class Scrapper:
  def SearchIdopeSe(search_query):
    r = []
    url = "https://idope.top/search/{}/".format(search_query)
    raw_html = requests.get(url).content
    soup = BeautifulSoup(raw_html, "html.parser")
    results = soup.find_all("div", {"class": "resultdiv"})
    for item in results:
      """ The content scrapped on 12.08.2018 22:00:45
      """
      title = item.find_all("div", {"class":"resultdivtopname"})[0].get_text().strip()
      hash = item.find_all("div", {"class":"resultdivbottonseed"})[0].get_text().strip()
      age = item.find_all("div", {"class":"resultdivbottontime"})[0].get_text().strip()
      size = item.find_all("div", {"class":"resultdivbottonlength"})[0].get_text().strip()
      r.append({
        "title": title,
        "hash": hash,
        "age": age,
        "size": size,
        "seeds": "NA",
        "peers": "NA"
      })
    return r

  def SearchTorrentz(search_query):
    r = []
    url = "https://torrentz2.eu/searchA?safe=1&f=" + search_query + ""
    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    raw_html = scraper.get(url).content
    # print(raw_html)
    soup = BeautifulSoup(raw_html, "html.parser")
    results = soup.find_all("div", {"class": "results"})[0]
    for item in results.find_all("dl"):
      # print(item)
      """The content scrapped on 23.06.2018 15:40:35
      """
      dt = item.find_all("dt")[0]
      dd = item.find_all("dd")[0]
      #
      try:
        link_and_text = dt.find_all("a")[0]
        link = link_and_text.get("href")[1:]
        title = link_and_text.get_text()
        span_elements = dd.find_all("span")
        date = span_elements[1].get_text()
        size = span_elements[2].get_text()
        seeds = span_elements[3].get_text()
        peers = span_elements[4].get_text()
        #
        r.append({
          "title": title,
          "hash": link,
          "date": date,
          "size": size,
          "seeds": seeds,
          "peers": peers
        })
      except:
        pass
    return r

  def GetMagneticLink(info_hash):
    name = "SpEcTorrentBot"
    trackers = [
      "udp://tracker.openbittorrent.com:80",
      "udp://opentor.org:2710",
      "udp://tracker.ccc.de:80",
      "udp://tracker.blackunicorn.xyz:6969",
      "udp://tracker.coppersurfer.tk:6969",
      "udp://tracker.leechers-paradise.org:6969",
      "udp://tracker.openbittorrent.com:80",
      "udp://tracker.publicbt.com:80",
      "udp://tracker.istole.it:80",
      "udp://tracker.btzoo.eu:80/announce",
      "http://opensharing.org:2710/announce",
      "udp://open.demonii.com:1337/announce",
      "http://announce.torrentsmd.com:8080/announce.php",
      "http://announce.torrentsmd.com:6969/announce",
      "http://bt.careland.com.cn:6969/announce",
      "http://i.bandito.org/announce",
      "http://bttrack.9you.com/announce",
    ];
    data = ""
    data += "magnet:"
    data += "?xt=urn:btih:"
    data += info_hash
    data += "&dn="
    data += urllib.parse.quote_plus(name)
    data += ""
    for tracker in trackers:
      data += "&tr="
      data += urllib.parse.quote_plus(tracker)
    return data
