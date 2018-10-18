# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from datetime import datetime
import requests
import mimetypes

current_date_time = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")


@bot.on(events.NewMessage(pattern=r".telegraph media", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(current_date_time):
        os.makedirs(current_date_time)
    if event.reply_to_msg_id:
        start = datetime.now()
        downloaded_file_name = await bot.download_media(
            await event.get_reply_message(),
            current_date_time
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to {} in {} seconds.".format(downloaded_file_name, ms))
        try:
            start = datetime.now()
            media_urls = upload_file(downloaded_file_name)
        except TelegraphException as e:
            await event.edit("ERROR: " + str(e))
            os.remove(downloaded_file_name)
        else:
            end = datetime.now()
            ms_two = (end - start).seconds
            os.remove(downloaded_file_name)
            await event.edit("Uploaded to {} in {} seconds.".format(media_urls[0], (ms + ms_two)))
    else:
        await event.edit("Reply to a message to get a permanent telegra.ph link. (Inspired by @ControllerBot)")


""" The below lines copied from https://github.com/python273/telegraph/blob/master/telegraph/upload.py
"""
def upload_file(f):
    """ Upload file to Telegra.ph's servers. Returns a list of links.
        Allowed only .jpg, .jpeg, .png, .gif and .mp4 files.

    :param f: filename or file-like object.
    :type f: file, str or list
    """
    with FilesOpener(f) as files:
        response = requests.post(
            'https://telegra.ph/upload',
            files=files
        ).json()

    if isinstance(response, list):
        error = response[0].get('error')
    else:
        error = response.get('error')

    if error:
        raise TelegraphException(error)

    return ["https://telegra.ph" + i['src'] for i in response]


class FilesOpener(object):
    def __init__(self, paths, key_format='file{}'):
        if not isinstance(paths, list):
            paths = [paths]

        self.paths = paths
        self.key_format = key_format
        self.opened_files = []

    def __enter__(self):
        return self.open_files()

    def __exit__(self, type, value, traceback):
        self.close_files()

    def open_files(self):
        self.close_files()

        files = []

        for x, file_or_name in enumerate(self.paths):
            name = ''
            if isinstance(file_or_name, tuple) and len(file_or_name) >= 2:
                name = file_or_name[1]
                file_or_name = file_or_name[0]

            if hasattr(file_or_name, 'read'):
                f = file_or_name

                if hasattr(f, 'name'):
                    filename = f.name
                else:
                    filename = name
            else:
                filename = file_or_name
                f = open(filename, 'rb')
                self.opened_files.append(f)

            mimetype = mimetypes.MimeTypes().guess_type(filename)[0]

            files.append(
                (self.key_format.format(x), ('file{}'.format(x), f, mimetype))
            )

        return files

    def close_files(self):
        for f in self.opened_files:
            f.close()

        self.opened_files = []


class TelegraphException(Exception):
    pass
