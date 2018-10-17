# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import subprocess
import requests
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError

from PIL import Image

current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./../DOWNLOADS/")


def progress(current, total):
    print("Downloaded {} of {}\nCompleted {}".format(current, total, (current / total) * 100))


@bot.on(events.NewMessage(pattern=r".download (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(current_date_time):
        os.makedirs(current_date_time)
    if event.reply_to_msg_id:
        start = datetime.now()
        downloaded_file_name = await bot.download_media(
            await event.get_reply_message(),
            current_date_time,
            progress_callback=progress
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        required_file_name = current_date_time + "" + file_name
        start = datetime.now()
        r = requests.get(url, stream=True)
        with open(required_file_name, "wb") as fd:
            total_length = r.headers.get('content-length')
            # https://stackoverflow.com/a/15645088/4723940
            if total_length is None: # no content length header
                fd.write(r.content)
            else:
                dl = 0
                total_length = int(total_length)
                for chunk in r.iter_content(chunk_size=128):
                    dl += len(chunk)
                    fd.write(chunk)
                    done = int(100 * dl / total_length)
                    download_progress_string = "Downloading ... [%s%s]" % ('=' * done, ' ' * (50-done))
                    # download_progress_string = "Downloading ... [%s of %s]" % (str(dl), str(total_length))
                    # download_progress_string = "Downloading ... [%s%s]" % ('⬛️' * done, '⬜️' * (100 - done))
                    """try:
                        await event.edit(download_progress_string)
                    except MessageNotModifiedError as e:
                        print("__FLOODWAIT__: {} sleeping for 100seconds, before proceeding.".format(str(e)))
                    time.sleep(1)"""
                    print(download_progress_string)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(required_file_name, ms))
    else:
        await event.edit("Reply to a message to download to my local server.")


@bot.on(events.NewMessage(pattern=r".upload (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        start = datetime.now()
        await bot.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id,
            progress_callback=progress
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Uploaded in {} seconds.".format(ms))
    else:
        await event.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen([
        'ffmpeg', '-i', file,
        '-ss', str(int((0, metadata.get('duration').seconds)[metadata.has('duration')] / 2)),
        '-filter:v', 'scale={}:-1'.format(width),
        '-vframes', '1',
        output,
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if not p.returncode and os.path.lexists(file):
        return output


def extract_w_h(file):
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        print(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@bot.on(events.NewMessage(pattern=r".uploadas(stream|vn) (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    type_of_upload = event.pattern_match.group(1)
    supports_streaming = False
    round_message = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    input_str = event.pattern_match.group(2)
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb = "1"
    if os.path.exists(file_name):
        start = datetime.now()
        metadata = extractMetadata(createParser(file_name))
        if thumb == "1":
            thumb_path = "a_random_f_file_name" + ".jpg"
            thumb = get_video_thumb(file_name, output=thumb_path)
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        # hachoir only works with MP4 files
        # this is good, since with MKV files sent as streamable Telegram responds,
        # Bad Request: VIDEO_CONTENT_TYPE_INVALID
        # if width is None or height is None:
        #     width, height = extract_w_h(file_name)
        """if os.path.exists(thumb):
            # width and height need to be the image width and height
            im = Image.open(thumb)
            # https://stackoverflow.com/a/6444612/4723940
            width, height = im.size"""
        try:
            if supports_streaming:
                await bot.send_file(
                    event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ],
                    progress_callback=progress
                )
            if round_message:
                await bot.send_file(
                    event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=0,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True
                        )
                    ],
                    progress_callback=progress
                )
            end = datetime.now()
            ms = (end - start).seconds
            os.remove(thumb)
            await event.edit("Uploaded in {} seconds.".format(ms))
        except FileNotFoundError as e:
            await event.edit(str(e))
    else:
        await event.edit("404: File Not Found")
