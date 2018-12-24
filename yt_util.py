import asyncio
import json
import urllib
import urllib.request

DEVELOPER_KEY = "AIzaSyCiBzYtWNgRXZWs5w2zqtp4Lqfve5GyGCY"

import json
import requests

DEVELOPER_KEY = "AIzaSyCiBzYtWNgRXZWs5w2zqtp4Lqfve5GyGCY"

def yt_search(q, maxResults):
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
        "duration": data["contentDetails"]["duration"]
    }
    
    return video
