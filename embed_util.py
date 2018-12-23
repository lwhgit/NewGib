def yt_list(videos):
    result = ""
    
    for i in range(0, len(videos)):
        result += str(i) + "|" + videos[i]["title"] + "|" + videos[i]["videoId"] + "\n"
        
    return result
