import json
import requests

def gt_tts(q, lang, path):
    results = requests.get("https://translate.google.com/translate_tts", 
        params = {
            "q": q,
            "ie": "UTF-8",
            "tl": lang,
            "client": "tw-ob"
        })
        
    return results.content
    '''
    f = open(path, "wb")
    f.write(results.content)
    f.close()'''
