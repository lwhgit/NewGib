# 유튜브 api 레퍼런스페이지에서 복붙해온 코드임. 뭐가뭔진 나도모름

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

DEVELOPER_KEY = "AIzaSyCiBzYtWNgRXZWs5w2zqtp4Lqfve5GyGCY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search(query, max_result):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_result
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append({
                "title": search_result["snippet"]["title"],
                "videoId": search_result["id"]["videoId"]
            });

    return videos
