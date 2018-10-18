import requests
import os
from datetime import datetime


current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")

@bot.on(events.NewMessage(pattern=r"\.stt (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("Downloading to my local, for analysis 🙇")
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        required_file_name = await bot.download_media(
            previous_message,
            current_date_time
        )
        lan = input_str
        if IBM_WATSON_CRED_USERNAME is None or IBM_WATSON_CRED_PASSWORD is None:
            await event.edit("You need to set the required ENV variables for this module. \nModule stopping")
        else:
            await event.edit("Starting analysis, using IBM WatSon Speech To Text")
            headers = {
                "Content-Type": previous_message.media.document.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize",
                headers=headers,
                data=data,
                auth=(IBM_WATSON_CRED_USERNAME, IBM_WATSON_CRED_PASSWORD)
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"]) + " + "
                    transcript_confidence += " " + str(alternatives["confidence"]) + " + "
                end = datetime.now()
                ms = (end - start).seconds
                string_to_show = "Language: `{}`\nTRANSCRIPT: `{}`\nTime Taken: {} seconds\nConfidence: `{}`".format(lan, transcript_response, ms, transcript_confidence)
                await event.edit(string_to_show)
            else:
                await event.edit(r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await event.edit("I do not know what to do with this message.")
