import requests
import os
import subprocess
from datetime import datetime
from gtts import gTTS


current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")


@bot.on(events.NewMessage(pattern=r".tts (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    else:
        lan, text = input_str.split("|")
    required_file_name = current_date_time + "voice.ogg"
    try:
        tts = gTTS(text, lan)
        tts.save(required_file_name)
        command_to_execute = [
            "ffmpeg",
            "-i",
             required_file_name,
             "-map",
             "0:a",
             "-codec:a",
             "libopus",
             "-b:a",
             "100k",
             "-vbr",
             "on",
             required_file_name + ".opus"
        ]
        try:
            t_response = subprocess.check_output(command_to_execute, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            await event.edit("process returned {}\n output: {}".format(input_str, exc.returncode, exc.output))
            # continue sending required_file_name
        except FileNotFoundErroras as exc:
            await event.edit("process returned {}\n output: {}".format(input_str, exc.returncode, exc.output))
            # continue sending required_file_name
        else:
            os.remove(required_file_name)
            required_file_name = required_file_name + ".opus"
        end = datetime.now()
        ms = (end - start).seconds
        await bot.send_file(
            event.chat_id,
            required_file_name,
            # caption="Processed {} ({}) in {} seconds!".format(text[0:97], lan, ms),
            reply_to=event.message.reply_to_msg_id,
            allow_cache=False,
            voice_note=True
        )
        os.remove(required_file_name)
        await event.edit("Processed {} ({}) in {} seconds!".format(text[0:97], lan, ms))
    except AssertionError as e:
        await event.edit(str(e))
