# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChannelBannedRights
from datetime import datetime, timedelta
from telethon.errors import UserAdminInvalidError
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently


@bot.on(events.NewMessage(pattern=".kick ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.edit("Getting Participant Lists. This might take some time ...")
    p = await bot.get_participants(event.chat_id, aggressive=True)
    await event.edit("Searching through {} users ...".format(len(p)))
    c = 0
    d = 0
    e = []
    m = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    for i in p:
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChannelBannedRights(
            until_date=None,
            view_messages=True
        )
        if i.deleted:
            d = d + 1
            if input_str == "d":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusEmpty:
            y = y + 1
            if input_str == "y":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusLastMonth:
            m = m + 1
            if input_str == "m":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusLastWeek:
            w = w + 1
            if input_str == "w":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusOffline:
            o = o + 1
            if input_str == "o":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusOnline:
            q = q + 1
            if input_str == "q":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusRecently:
            r = r + 1
            if input_str == "r":
                try:
                    await bot(EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
    required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
    """
    await event.edit(required_string.format(c, len(p), d, y, m, w, o, q, r))
