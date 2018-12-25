import asyncio
import discord
import embed_util

class BotData:
    def __init__(self):
        self.ready = False
        self.servers = {}
        
    def add_server_data(self, client, server):
        serverId = server.id
        self.servers[str(server.id)] = ServerData(client, server)
        return self.servers[str(server.id)]
        
    def get_server_data(self, server):
        server_data = self.servers[str(server.id)]
        if (server_data == None):
            print("  Wrong server data request.")
            return None
        else:
            return server_data
            
    def get_server_data_list(self):
        return list(self.servers.values())

class ServerData:
    def __init__(self, client, server):
        self.client = client
        self.server = server
        self.res_path = "\\res\\" + server.name
        self.channels = list(server.channels)
        self.voice_client = None
        self.text_channels = []
        self.voice_channels = []
        self.current_text_channel = None
        self.tts_player = None
        self.yt_player = None
        self.yt_player_started = False
        self.yt_player_paused = False
        self.yt_player_done = False
        self.yt_play_list = []
        self.yt_play_list_index = 0
        self.yt_search_list = []
        
        
        for i in range(0, len(self.channels)):
            channel = self.channels[i]
            if (channel.type == discord.ChannelType.text):
                self.text_channels.append(channel)
            elif (channel.type == discord.ChannelType.voice):
                self.voice_channels.append(channel)
                
        self.show_server_data()
        
        
    def show_server_data(self):
        print("  Server Data")
        print("    Name: " + self.server.name)
        print("    Channels:")
        self.show_channels_data()
        
    def show_channels_data(self):
        print("      Text Cahnnels:")
        for i in range(0, len(self.text_channels)):
            channel = self.text_channels[i]
            print("        Channel Data")
            print("          Name: " + channel.name)
            print("          Type: Text")
            
        print("      Voice Cahnnels:")
        for i in range(0, len(self.voice_channels)):
            channel = self.voice_channels[i]
            print("        Channel Data")
            print("          Name: " + channel.name)
            print("          Type: Voice")
            
    def get_text_channels(self):
        return self.text_channels
        
    def get_voice_channels(self):
        return self.voice_channels
        
    async def send_message(self, content=None, embed=None):
        return await self.client.send_message(self.current_text_channel, content=content, embed=embed)
        
    async def edit_message(self, message, new_content=None, embed=None):
        return await self.client.edit_message(message, new_content=new_content, embed=embed)
        
    def on_yt_player_after(self):
        if (self.yt_player.is_done()):
            self.yt_player_done = True
            print("done")
        
    async def start_yt_player(self):
        video = self.yt_play_list[self.yt_play_list_index]
        self.yt_player = "tmp string"
        self.yt_player_started = True
        self.yt_player = await self.voice_client.create_ytdl_player(video["url"], after=self.on_yt_player_after)
        self.yt_player.start()
        self.yt_player_done = False
        await self.send_message("재생중", embed=embed_util.yt_detail(video))
        
    async def start_yt_player_at(self, index):
        if (index < len(self.yt_play_list)):
            self.yt_play_list_index = index
            if (self.is_yt_player_playing()):
                self.stop_yt_player()
                
            await self.start_yt_player()
        else:
            print("  Wrong play list index!")
            
    async def start_yt_player_next(self):
        if (self.is_exists_yt_play_list()): 
            self.yt_play_list_index += 1
            if (self.yt_play_list_index >= len(self.yt_play_list)):
                self.yt_play_list_index = 0
                
            await self.start_yt_player_at(self.yt_play_list_index)
        
    async def add_yt_play_list(self, video, notice=False):
        if (notice):
            await self.send_message("재생목록에 추가할게요.", embed=embed_util.yt_detail(video))
        self.yt_play_list.append(video)
        
    def stop_yt_player(self):
        self.yt_player.stop()
        self.yt_player = None
        self.yt_player_started = False
        
    def pause_yt_player(self):
        self.yt_player.pause()
        self.yt_player_paused = True
        
    def resume_yt_player(self):
        if (self.is_yt_player_paused()):
            self.yt_player.resume()
            self.yt_player_paused = False
        
    def is_yt_player_playing(self):
        if (self.yt_player != None):
            return self.yt_player.is_playing()
        else:
            return False
            
    def is_yt_player_stopped(self):
        return self.yt_player_started == False
        
            
    def is_yt_player_paused(self):
        if (self.yt_player != None):
            return self.yt_player_paused
        else:
            return False
            
    def is_yt_player_done(self):
        return self.yt_player_done
        
    def get_yt_play_list_size(self):
        return len(self.yt_play_list)
        
    def get_yt_play_list(self):
        return self.yt_play_list
        
    def is_exists_yt_play_list(self):
        return len(self.yt_play_list) > 0
        
    def get_current_play_list_index(self):
        if (self.yt_play_list_index >= len(self.yt_play_list)):
            self.yt_play_list_index = 0
            
        return self.yt_play_list_index
        
    def get_yt_play_list_embed(self):
        return embed_util.yt_play_list(self.yt_play_list)
        
    def set_yt_search_list(self, list):
        self.yt_search_list = list
        
    def get_yt_search_list(self):
        return self.yt_search_list
        
    def get_yt_search_list_size(self):
        return len(self.yt_search_list)
    
    def play_tts(self, dir):
        self.tts_player = self.voice_client.create_ffmpeg_player(dir)
        self.tts_player.start()
