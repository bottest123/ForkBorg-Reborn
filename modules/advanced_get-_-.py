from functools import partial
from uniborg import util


@bot.on(events.NewMessage(pattern=r"(?i)^\.aget (.*)$"))
async def _(event):
    if await util.isAdmin(event):
        await util.run_and_upload(
            event=event,
            to_await=partial(
                util.simple_run, command=event.pattern_match.group(1)),
            quiet=False)
