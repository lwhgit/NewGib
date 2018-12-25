import json
import requests

DEVELOPER_KEY = "AIzaSyCiBzYtWNgRXZWs5w2zqtp4Lqfve5GyGCY"
YOUTUBE_LINK = "https://www.youtube.com/watch?v="

def yt_search(q, maxResults):
    
    maxResults += 1
    
    results = requests.get("https://www.googleapis.com/youtube/v3/search", 
        params = {
            "q": q,
            "maxResults": maxResults,
            "part": "id,snippet",
            "key": DEVELOPER_KEY
        })


    data = results.json()["items"]
    
    videos = []

    for video in data:
        if (video["id"]["kind"] == "youtube#video"):
            videos.append({
                "title": video["snippet"]["title"],
                "thumbnails": video["snippet"]["thumbnails"],
                "videoId": video["id"]["videoId"]
            });

    return videos

def yt_video(videoId):
    results = requests.get("https://www.googleapis.com/youtube/v3/videos", 
        params = {
            "id": videoId,
            "part": "id,snippet,contentDetails",
            "key": DEVELOPER_KEY
        })


    data = results.json()["items"][0]
    
    video = {
        "title": data["snippet"]["title"],
        "thumbnails": data["snippet"]["thumbnails"],
        "videoId": data["id"],
        "url": YOUTUBE_LINK + data["id"],
        "duration": yt_pt2time(data["contentDetails"]["duration"])
    }
    
    return video
    
def yt_pt2time(str):
    cnt = 0
    result = ""
    idx = [0,0,0]
    idx[0] = str.find('H')
    idx[1] = str.find('M')
    idx[2] = str.find('S')
    d = str.replace("PT", "").replace('M', 'H').replace('S', 'H').split('H')
    if (idx[0] != -1):
        result = d[cnt] + ':'
        cnt += 1
    if (idx[1] != -1):
        if (len(d[cnt]) == 1):
            d[cnt] = "0" + d[cnt]
        result = result + d[cnt] + ':'
        cnt += 1
    elif (cnt != 0):
        result = result + "00:"
    if (idx[2] != -1):
        if (len(d[cnt]) == 1):
            d[cnt] = "0" + d[cnt]
        result = result +  d[cnt]
    elif (cnt != 0):
        result = result + "00"
    return result
