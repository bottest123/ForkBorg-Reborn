# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import traceback

from uniborg import util
from datetime import datetime

DELETE_TIMEOUT = 2


@bot.on(util.admin_cmd(r"^\.load (?P<shortname>\w+)$"))
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]

    try:
        if shortname in bot._plugins:
            bot.remove_plugin(shortname)
        bot.load_plugin(shortname)

        msg = await event.respond(
            f"Successfully (re)loaded plugin {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await bot.delete_messages(msg.to_id, msg)

    except Exception as e:
        tb = traceback.format_exc()
        logger.warn(f"Failed to (re)load plugin {shortname}: {tb}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


@bot.on(util.admin_cmd(r"^\.(?:unload|remove) (?P<shortname>\w+)$"))
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]

    if shortname == "_core":
        msg = await event.respond(f"Not removing {shortname}")
    elif shortname in bot._plugins:
        bot.remove_plugin(shortname)
        msg = await event.respond(f"Removed plugin {shortname}")
    else:
        msg = await event.respond(f"Plugin {shortname} is not loaded")

    await asyncio.sleep(DELETE_TIMEOUT)
    await bot.delete_messages(msg.to_id, msg)


@bot.on(util.admin_cmd(r"^\.send plugin (?P<shortname>\w+)$"))
async def load_reload(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./modules/{}.py".format(input_str)
    start = datetime.now()
    await bot.send_file(
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id
    )
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Uploaded {} in {} seconds".format(input_str, ms))
