import asyncio
import requests
import json


@bot.on(events.NewMessage(pattern=r"\.github (.*)"))
@bot.on(events.MessageEdited(pattern=r"\.github (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    url = "https://api.github.com/users/{}".format(input_str)
    r = requests.get(url)
    if r.status_code != 404:
        b = r.json()
        avatar_url = b["avatar_url"]
        html_url = b["html_url"]
        gh_type = b["type"]
        name = b["name"]
        company = b["company"]
        blog = b["blog"]
        location = b["location"]
        bio = b["bio"]
        created_at = b["created_at"]
        await event.edit("""[\u2063]({})Name: [{}]({})
Type: {}
Company: {}
Blog: {}
Location: {}
Bio: {}
Profile Created: {}""".format(avatar_url, name, html_url, gh_type, company, blog, location, bio, created_at))
    else:
        await event.edit("`{}`: {}".format(input_str, r.text))
