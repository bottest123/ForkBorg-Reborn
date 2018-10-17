from telethon.tl.functions.messages import GetInlineBotResultsRequest
from telethon.tl.functions.messages import SendInlineBotResultRequest
from telethon.errors import BotTimeout


@bot.on(events.NewMessage(pattern=r"\.ib (.[^ ]*) (.*)", outgoing=True))
async def _(event):
    # https://stackoverflow.com/a/35524254/4723940
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    search_query = event.pattern_match.group(2)
    try:
        bot_results = await bot(GetInlineBotResultsRequest(
            bot_username, event.chat_id, search_query, ''
        ))
        if len(bot_results.results) > 0:
            await bot(SendInlineBotResultRequest(
                event.chat_id,
                bot_results.query_id,
                bot_results.results[0].id,
                reply_to_msg_id=event.message.reply_to_msg_id
            ))
            await event.delete()
        else:
            await event.edit("{} did not respond correctly, for **{}**!".format(bot_username, search_query))
    except BotTimeout as e:
        await event.edit("{} did not respond correctly, for **{}**!\n `{}`".format(bot_username, search_query, str(e)))



