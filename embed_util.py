import discord

YOUTUBE_LINK = "https://www.youtube.com/watch?v="

def yt_list(videos):
    embed = discord.Embed()
    for i in range(0, len(videos)):
        embed.add_field(name=str(i + 1) + "  " + videos[i]["title"], value=YOUTUBE_LINK + videos[i]["videoId"])
        
    return embed
    
def yt_detail(video):
    embed = discord.Embed(title=video["title"] + "``" + video["duration"] + "``", description=YOUTUBE_LINK + video["videoId"])
    embed.set_thumbnail(url=video["thumbnails"]["default"]["url"])
    
    return embed
