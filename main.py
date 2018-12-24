#https://discordapp.com/oauth2/authorize?client_id=472406585222758401&scope=bot

# 참고로 라이브러리 필수

import asyncio
import discord
import time
import os
import subprocess
import threading

import yt_util
import embed_util

from bot_data import BotData

PATH = os.path.dirname(os.path.realpath(__file__))  # main.py 위치
client = discord.Client()
bot_data = BotData()

TOKEN = [
    {
        "name": "Gib_beta",
        "token": "NDcyNDA2NTg1MjIyNzU4NDAx.Dj31AA.tr1iAfTuiBfNw8jGAzcc5gABfSk"
    }
]
'''
async def printHelp(message):    # 도움말을 출력합니다
    await client.send_message(message.channel, "집 도움말　　　　　　: 도움말을 출력합니다.")
    print("집 도움말　　　　　　: 도움말을 출력합니다.") # 근데 이렇게하면 콘솔에 뜨는데?
    print("집 핑　　　　　　　　: 집이 살아있는지 확인합니다.")
    print("집 나가　　　　　　　: 집을 보이스채널에서 추방합니다.")
    print("집 꺼져　　　　　　　: 집을 로그아웃 시킵니다.")
    print("집 말해 ［메세지］　 : Text To Speech로 음성메세지를 전달합니다.")
    print("도움말 : 도움말을 출력합니다.")'''

@client.event
async def on_ready():
    print(client.user.name) # 이거 딱히 필요한가
    print(client.user.id)
    
    servers = list(client.servers)
    
    for i in range(0, len(servers)):
        bot_data.add_server_data(servers[i])
        
    
@client.event
async def on_message(message):
    global bot_data
    
    server_data = bot_data.get_server_data(message.server)
    
    msg_content = message.content # 메세지
    voice_client = message.server.voice_client # 뭔지 까먹음 이게 뭐더라 ㄹㅇ
    author_voice_channel = message.author.voice_channel # 채팅 한 사람의 보이스 채널
    bot_voice_channel = None
    if (voice_client != None):
        bot_voice_channel = voice_client.channel
        
    cmd = msg_content.split(" ")
    cmdLen = len(cmd)
    
    if (message.author.bot):
        return;
        
    print("    CHAT  |IN [" + message.server.name + "]|  " + str(message.timestamp) + "|" + message.author.name + ": " + message.content)
        
#    집으로 시작하는가
#        매개변수가 1개인가
#            명령
#        매개변수가 2개이상인가
#            매개변수 1이 무엇인가
#            ...
#        매개변수가 3개이상인가
#            매개변수 1이 무엇인가
#                매개변수 2이 무엇인가
#                    명령
#                ...
#            ...
#        ...

    if (cmd[0] == "집"):
        if (cmdLen == 1):
            pass
        if (cmdLen >= 2):
            if (cmd[1] == "도움말"):
                await printHelp(message)

            elif (cmd[1] == "꺼져"):
                if (data.message.author.name == "lwh"):
                    await client.logout()

        if (cmdLen >= 3):
            if (cmd[1] == "유튜브"):
                query = msg_content.split("집 유튜브")[1]
                print("    cmd: 유튜브")
                print("    query: " + query)
                
                videoId = yt_util.yt_search(query, 1)[0]["videoId"]
                video = yt_util.yt_video(videoId);
                
                yt_detail_embed = embed_util.yt_detail(video)
                
                await client.send_message(message.channel, embed=yt_detail_embed)
            
            elif (cmd[1] == "유튜브검색"):
                query = msg_content.split("집 유튜브검색")[1]
                print("    cmd: 유튜브검색")
                print("    query: " + query)
                
                videos = yt_util.search(query, 10)
                
                yt_list_embed = embed_util.yt_list(videos)
                
                await client.send_message(message.channel, embed=yt_list_embed)

        
@client.event
async def on_voice_state_update(before, after):
    pass
    
def login(index):   # 이거 호출하면 집 로그인 됨, login(0) 으로 부르면 될듯
    
    client.run(TOKEN[index]["token"])

login(0);

#근데 봇 상태를 기록할 객체가 필요함
#여러 서버 들어가도 한 코드에서 직렬로 실행되니까 객체지향 필수
#https://discordpy.readthedocs.io/en/latest/api.html#event-reference 참고하셈
