# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto


@bot.on(events.NewMessage(pattern=r".get_id", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        r_msg = await event.get_reply_message()
        if r_msg.media:
            type_of_media = type(r_msg.media)
            bot_api_file_id = None
            if type_of_media == MessageMediaDocument:
                bot_api_file_id = "NA" # b64encode(rle_encode())
            elif type_of_media == MessageMediaPhoto:
                bot_api_file_id = "NA"
            await event.edit("The BOT API file ID of this media is `{}`!".format(str(bot_api_file_id)))
        else:
            chat = await event.get_input_chat()
            await event.edit("The current chat's ID is `{}`!".format(str(event.chat_id)))
    else:
        chat = await event.get_input_chat()
        await event.edit("The current chat's ID is `{}`!".format(str(event.chat_id)))


# File ported from @danog's repo to Python by @Lonami (@LonamiWebs):
# https://github.com/danog/MadelineProto/blob/d3cff5e0afdf625e1c83d5d6531dd463f112bbb5/src/danog/MadelineProto/TL/Conversion/BotAPIFiles.php
import struct
from base64 import b64decode, b64encode


TYPES = {  # or so it seems
    2: 'photo',
    3: 'voice',
    10: 'document/video',
    13: 'document/video_note'
}


def b64url_decode(data):
    data = data.replace(b'-', b'+').replace(b'_', b'/')
    return b64decode(data + b'=' * (len(data) % 4))


def b64url_encode(data):
    return b64encode(data.replace(b'+', b'-').replace(b'/', b'_')).rstrip(b'=')


def rle_decode(string):
    new = b''
    last = b''
    null = b'\0'
    for cur in string:
        cur = bytes([cur])
        if last == null:
            new += last * ord(cur)
            last = b''
        else:
            new += last
            last = cur

    string = new + last
    return string


def rle_encode(string):
    new = b''
    count = 0
    null = b'\0'
    for cur in string:
        if cur == null:
            count += 1
        else:
            if count > 0:
                new += null + bytes([count])
                count = 0
            else:
                new += cur
    return new


def unpack_file_id(file_id):
    file_id = rle_decode(b64url_decode(file_id.encode('ascii')))
    assert file_id[-1] != b'\x02'
    file_id = file_id[:-1]
    assert len(file_id) in (24, 44)

    if len(file_id) == 24:
        # Document
        file_type, dc_id, media_id, access_hash = struct.unpack('<iiqq', file_id)
    else:
        # Photo
        file_type, dc_id, media_id, access_hash, volume_id, secret, local_id = struct.unpack(
            '<iiqqqqi', file_id
        )

    print(file_type, dc_id)
    if file_type == 2:
        # Photo
        pass

    return media_id, access_hash


DANIIL_COMMENT = '''
How bot file IDs work:

It's basically, for documents:
    base64(rle(type + DC_id + id + access hash))

And for photos:
    base64(rle(type + DC_id + id + access hash
               + PhotoSize volume id + PhotoSize secret + PhotoSize local id))

Here the access hash and the ID can be just 0 if you only want
to download the file, and for thumbnails it is always 0.

The types:
0 - thumbnail
2 - photo
3 - voice
4 - video
5 - any other document

RLE (https://en.wikipedia.org/wiki/Run-length_encoding) is based on null byte.
The last byte is always 2 and is used for error checking.
'''

