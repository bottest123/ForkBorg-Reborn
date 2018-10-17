from telethon.tl.types import SendMessageRecordAudioAction, \
    SendMessageRecordVideoAction, SendMessageUploadAudioAction, \
    SendMessageUploadPhotoAction, SendMessageUploadVideoAction, \
    SendMessageRecordRoundAction, SendMessageTypingAction, SendMessageUploadDocumentAction
from telethon.tl.functions.messages import SetTypingRequest
import random


@bot.on(events.NewMessage(pattern=r"\.sca ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    actions = {}
    actions["ra"] = SendMessageRecordAudioAction()
    actions["rv"] = SendMessageRecordVideoAction()
    actions["ua"] = SendMessageUploadAudioAction(0)
    actions["up"] = SendMessageUploadPhotoAction(0)
    actions["uv"] = SendMessageUploadVideoAction(0)
    actions["rr"] = SendMessageRecordRoundAction()
    actions["mt"] = SendMessageTypingAction()
    actions["ud"] = SendMessageUploadDocumentAction(0)
    action = actions["mt"]
    if input_str:
        action = actions[input_str]
    await bot(SetTypingRequest(event.chat_id, action))
    await event.delete()

