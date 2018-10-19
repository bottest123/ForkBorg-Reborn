import os


@bot.on(events.NewMessage(pattern=r"\.fwd", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if PRIVATE_CHANNEL_BOT_API_ID is not None:
        try:
            e = await borg.get_entity(int(PRIVATE_CHANNEL_BOT_API_ID))
        except e:
            await event.edit(str(e))
            return None
        re_message = await event.get_reply_message()
        # https://t.me/telethonofftopic/78166
        fwd_message = await borg.forward_messages(
            e,
            re_message,
            silent=True
        )
        await borg.forward_messages(
            event.chat_id,
            fwd_message
        )
        await fwd_message.delete()
        await event.delete()
    else:
        await event.edit("Please set the required environment variables for this plugin to work")
