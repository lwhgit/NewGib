#https://discordapp.com/oauth2/authorize?client_id=472406585222758401&scope=bot

# 참고로 라이브러리 필수

import asyncio
import discord
import time
import os
import subprocess
import threading

import yt_util
import gt_util
import nendic_util
import embed_util

from bot_data import BotData

PATH = os.path.dirname(os.path.realpath(__file__))  # main.py 위치
client = discord.Client()
bot_data = BotData()

TOKEN = [
    {
        "name": "Gib_beta",
        "token": "NDcyNDA2NTg1MjIyNzU4NDAx.Dj31AA.tr1iAfTuiBfNw8jGAzcc5gABfSk"
    }, {
        "name": "LwhTest",
        "token": "NDE3MjQ4NzM4OTIzMzgwNzM2.Dj7CeA.mIlZyfgS7htnt-5LJON7-UuyACk",
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
    global bot_data
    
    print(client.user.name) # 이거 딱히 필요한가
    print(client.user.id)
    
    servers = list(client.servers)
    
    for i in range(0, len(servers)):
        server_data = bot_data.add_server_data(client, servers[i])
        await client.join_voice_channel(server_data.get_voice_channels()[0])
        
        dir = PATH + server_data.res_path
        if (os.path.isdir(dir) == False):
            os.mkdir(dir)
            
    bot_data.ready = True
    
    await bot_manager_thread()
        
        
@client.event
async def on_message(message):
    global bot_data
    
    if (bot_data.ready == False):
        return
    
    server_data = bot_data.get_server_data(message.server)
    server_data.current_text_channel = message.channel
    
    msg_content = message.content # 메세지
    server_data.voice_client = message.server.voice_client # 말그대로 해당 서버의 보이스 클라같음. 그러니까 그쪽 보이스에 뭐 하고싶으면 이게 필요함.
    author_voice_channel = message.author.voice_channel # 채팅 한 사람의 보이스 채널
    bot_voice_channel = None
    if (server_data.voice_client != None):
        bot_voice_channel = server_data.voice_client.channel
        
    cmd = msg_content.split(" ")
    cmdLen = len(cmd)
    
    if (message.author.bot):
        return;
        
    print("    CHAT  |IN [" + message.server.name + "]|  " + str(message.timestamp) + "|" + message.author.name + ": " + message.content)

    if (cmd[0] == "집"):
        if (cmdLen == 1):
            pass
        if (cmdLen >= 2):
            if (cmd[1] == "핑"):
                await server_data.send_message("퐁")
                
            elif (cmd[1] == "도움말"):
                await printHelp(message)

            elif (cmd[1] == "꺼져"):
                if (message.author.name == "lwh"):
                    await client.logout()
                    
            elif (cmd[1] == "정지"):
                if (server_data.yt_player != None):
                    server_data.stop_yt_player()
                else:
                    await server_data.send_message("재생중이지 않았습니다.")
                
            elif (cmd[1] == "일시정지"):
                if (server_data.is_yt_player_playing()):
                    server_data.pause_yt_player()
                else:
                    await server_data.send_message("재생중이지 않았습니다.")
                    
                    
            elif (cmd[1] == "다음"):
                await server_data.start_yt_player_next()
                
            elif (cmd[1] == "재생목록"):
                yt_play_list_embed = server_data.get_yt_play_list_embed()
                await server_data.send_message(embed=yt_play_list_embed)
                    
            elif (cmd[1] == "재생"):
                if (server_data.is_yt_player_paused()):
                    server_data.yt_player.resume()
                elif (server_data.is_yt_player_playing()):
                    await server_data.send_message("재생중 이었습니다.")
                elif (server_data.is_yt_player_stopped()):
                    if (server_data.get_yt_play_list_size() == 0):
                        await server_data.send_message("재생할 리스트가 없습니다.")
                    elif (server_data.get_yt_play_list_size() > 0):
                        video = server_data.get_yt_play_list()[server_data.get_current_play_list_index()]
                        yt_detail_embed = embed_util.yt_detail(video)
                        
                        msg = await client.send_message("재생 대기중...")
                        await server_data.start_yt_player()
                    
        if (cmdLen >= 3):
            if (cmd[1] == "유튜브"):
                query = msg_content.split("집 유튜브")[1]
                print("    cmd: 유튜브")
                print("    query: " + query)
                
                msg = await server_data.send_message("검색 시작...")
                
                videoId = yt_util.yt_search(query, 1)[0]["videoId"]
                video = yt_util.yt_video(videoId);
                
                yt_detail_embed = embed_util.yt_detail(video)
                
                await server_data.edit_message(msg, new_content="재생 대기중...")
                
                if (server_data.is_yt_player_stopped()):
                    await server_data.add_yt_play_list(video, False)
                    await server_data.start_yt_player()
                else:
                    await server_data.edit_message(msg, new_content="이미 재생중입니다.")
                    await server_data.add_yt_play_list(video, True)
            
            elif (cmd[1] == "유튜브검색"):
                query = msg_content.split("집 유튜브검색")[1]
                print("    cmd: 유튜브검색")
                print("    query: " + query)
                
                videos = yt_util.yt_search(query, 10)
                
                yt_list_embed = embed_util.yt_search_list(videos)
                
                await server_data.send_message(embed=yt_list_embed)
                
                server_data.set_yt_search_list(videos)
                
            elif (cmd[1] == "선택"):
                select = int(msg_content.split("집 선택 ")[1])
                
                if (select < 1 or select > server_data.get_yt_search_list_size()):
                    await server_data.send_message("그렇게 선택할 수 없습니다.")
                else:
                    videoId = server_data.get_yt_search_list()[select - 1]["videoId"]
                    video = yt_util.yt_video(videoId);
                    
                    yt_detail_embed = embed_util.yt_detail(video)
                    
                    msg = await server_data.send_message("재생 대기중...")
                    
                    if (server_data.is_yt_player_stopped()):
                        await server_data.add_yt_play_list(video, False)
                        await server_data.start_yt_player()
                    else:
                        await server_data.edit_message(msg, new_content="이미 재생중입니다.")
                        await server_data.add_yt_play_list(video, True)
                
            elif (cmd[1] == "tts"):
                query = msg_content.split("집 tts")[1]
                print("    cmd: tts")
                print("    query: " + query)
                
                tts = gt_util.gt_tts(query, "ko", "")
                
                path = PATH + server_data.res_path + "\\tts.mp3"
                save_file(path, "wb", tts)
                
                server_data.play_tts(path)
                
            elif (cmd[1] == "영단어"):
                query = msg_content.split("집 영단어")[1]
                print("    cmd: 영단어")
                print("    query: " + query)

                result = nendic_util.nendic_search(query)
                
                if (result == -1):
                    await server_data.send_message("``" + query + "`` 에 대한 결과를 찾을 수 없습니다.")
                else:
                    await server_data.send_message("``" + query + "`` 에 대한 결과입니다.\n```\n" + result + "```")
        
@client.event
async def on_voice_state_update(before, after):
    pass
    
async def bot_manager_thread():
    global bot_data
    
    while (True):
        try:
            for server_data in bot_data.get_server_data_list():
                if (server_data.is_yt_player_done()):
                    print("next")
                    await server_data.start_yt_player_next()
            
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(1)
    
def login(index):   # 이거 호출하면 집 로그인 됨, login(0) 으로 부르면 될듯
    client.run(TOKEN[index]["token"])

def save_file(path, mode, content):
    f = open(path, mode)
    f.write(content)
    f.close()
    

login(0)
#https://discordpy.readthedocs.io/en/latest/api.html#event-reference 참고하셈
