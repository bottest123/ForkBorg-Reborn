# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
import urllib3
import json
import certifi

@bot.on(events.NewMessage(pattern=r".xtools (.*)", outgoing=True))
async def _(event):
		if event.fwd_from:
			return
		input_str = event.pattern_match.group(1)
		start = datetime.now()
		if event.reply_to_msg_id:
			previous_message = await event.get_reply_message()
			username = previous_message.message
			lan = input_str
		else:
			lan, username = input_str.split("|")
    
		url = 'https://xtools.wmflabs.org/api/user/simple_editcount/'
		project = lan+'.wikipedia.org/'
		final_url = url+project+username
		https= urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
		r = https.request('GET', final_url)
		json_string = json.loads(r.data)
		result_text = json_string['liveEditCount']
		#print ("elapsed_time", json_string['elapsed_time'])
		end = datetime.now()
		ms = (end - start).seconds
		output_str = "edit count {} in {} seconds. \n {}".format(lan, str(ms),result_text)
		await event.edit(output_str)
