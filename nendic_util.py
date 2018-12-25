import json
import requests

def nendic_search(q):
    results = requests.get("https://ac.dict.naver.com/enendict/ac", 
        params = {
            "q": q,
            "q_enc": "utf-8",
            "st": "11001",
            "r_format": "json",
            "r_enc": "utf-8",
            "r_lt": "11001",
            "r_unicode": "0",
            "r_esacpe": "1",
        })

    
    data = results.json()["items"]
    
    if (len(data[0]) == 0):
        return -1
    else:
        return data[0][0][1][0]
