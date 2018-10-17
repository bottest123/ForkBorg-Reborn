# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

import random, re

@bot.on(events.NewMessage(pattern=r".decide", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    r = random.randint(1, 100)
    if r % 3 == 1:
        await event.edit("Yes")
    elif r % 3 == 2:
        await event.edit("No")
    else:
        await event.edit("¯\_(ツ)_/¯")

