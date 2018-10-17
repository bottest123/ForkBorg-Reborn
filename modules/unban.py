from telethon.tl.types import ChannelParticipantsAdmins, ChannelParticipantsKicked, ChannelBannedRights
from telethon.errors import ChatAdminRequiredError, InputUserDeactivatedError, FloodWaitError
from telethon.tl.functions.channels import EditBannedRequest
import asyncio


@bot.on(events.NewMessage(pattern=".unbanall ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    # Note that it's "reversed". You must set to ``True`` the permissions
    # you want to REMOVE, and leave as ``None`` those you want to KEEP.
    rights = ChannelBannedRights(
        until_date=None,
        view_messages=True
    )
    input_str = event.pattern_match.group(1)
    print(input_str)
    to_write_chat = await event.get_input_chat()
    chat = None
    if not input_str:
        chat = to_write_chat
    else:
        try:
            chat = await bot.get_entity(input_str)
        except ValueError as e:
            await event.edit(str(e))
            return None
    c = 0
    print(chat)
    try:
        async for x in bot.iter_participants(chat, filter=ChannelParticipantsKicked):
            try:
                await bot(EditBannedRequest(chat, x, rights))
                c = c + 1
                print(c)
                await asyncio.sleep(1)
            except FloodWaitError as e:
                await event.edit(str(e))
                await asyncio.sleep(10)
    except ChatAdminRequiredError as e:
        await event.edit(str(e))
    await event.edit("unbanned {} users".format(c))

