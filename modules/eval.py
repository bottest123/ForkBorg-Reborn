# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0

import inspect
from telethon.errors import MessageEmptyError
import os

MAX_MESSAGE_SIZE_LIMIT = 4095
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./downloads/")


@bot.on(events.NewMessage(pattern=r"\.eval1 (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    cmd = event.pattern_match.group(1)
    evaluation = None
    # https://t.me/telethonofftopic/43873
    try:
        if inspect.isawaitable(eval(cmd)):
            evaluation = await eval(cmd)
        # https://t.me/telethonofftopic/43873
        else:
            evaluation = eval(cmd)
    except (ZeroDivisionError, ValueError, SyntaxError, AttributeError) as e:
        evaluation = str(e)
    # https://t.me/telethonofftopic/43873
    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        current_file_name = "{}temp_file.text".format(TEMP_DOWNLOAD_DIRECTORY)
        file_ponter = open(current_file_name, "w+")
        file_ponter.write(final_output)
        file_ponter.close()
        await bot.send_file(
            event.chat_id,
            current_file_name,
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id
        )
        await event.delete()
        os.remove(current_file_name)
    else:
        await event.edit(final_output)
