# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time


@bot.on(events.NewMessage(pattern=r".emoji (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 16)
    input_str = event.pattern_match.group(1)
    if input_str == "shrug":
        await event.edit("¯\_(ツ)_/¯")
    elif input_str == "apple":
        await event.edit("\uF8FF")
