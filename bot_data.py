import discord

class BotData:
    def __init__(self):
        self.servers = {}
        
    def add_server_data(self, server):
        serverId = server.id
        self.servers[str(server.id)] = ServerData(server)
        pass
        
    def get_server_data(self, server):
        server_data = self.servers[str(server.id)]
        if (server_data == None):
            print("  Wrong server data request.")
            return None
        else:
            return server_data

class ServerData:
    def __init__(self, server):
        self.server = server
        self.channels = list(server.channels)
        self.text_channels = []
        self.voice_channels = []
        self.yt_player = None
        self.yt_play_list = []
        
        
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
        
