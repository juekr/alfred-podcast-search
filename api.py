import requests
from decouple import config
import time
import hashlib
import json
import sys
import os
import requests_cache
# import podcastparser
# import io
# import datetime

class Podcasttools:
    podcastindex = {
        "api key": '',
        "api secret" : '',
        "base url" : "https://api.podcastindex.org/api/1.0/search/byterm?q=" 
    }

    podcastCacheName = "podcast-xml-cache"
    podcastCacheExpiration = 60*60*12

    def __init__(self, config_loader):
        self.podcastindex["api key"] = config_loader("PODCASTINDEX_API_KEY")
        self.podcastindex["api secret"] = config_loader("PODCASTINDEX_API_SECRET")
        requests_cache.install_cache(self.podcastCacheName, expire_after=self.podcastCacheExpiration)
        

    def searchWithPodcastIndex(self, search_for):
        epoch_time = int(time.time())
        data_to_hash = self.podcastindex["api key"] + self.podcastindex["api secret"] + str(epoch_time)
        sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
        headers = {
            'X-Auth-Date': str(epoch_time),
            'X-Auth-Key': self.podcastindex["api key"],
            'Authorization': sha_1,
            'User-Agent': 'postcasting-index-python-cli'
        }
        return requests.post(f"{self.podcastindex['base url']}{search_for}", headers=headers)

        
    def searchPodcast(self, search_for:str = ""):
        """Searches PODCASTINDEX for string

        Args:
            search_for (str, optional): _description_. Defaults to "".

        Returns:
            list: [{ title, description, feed, originalUrl, author, owner, language, generator, id_podcastindex, id_apple, fetched, source }]
        """
        # Return empty list for empty search terms
        if not search_for: return []

        # Check whether search term is an integer (= apple podcast id) or a term (string)
        # todo: make use of this
        try:
            search_for = int(search_for)
        except Exception:
            #print("No podcast id set, searching titles instead")
            search_for = str(search_for)
        
        # query podcastindex API
        resultPI = self.searchWithPodcastIndex(search_for)

        # build result
        listReturn = []
        if resultPI.status_code == 200:
            feeds = json.loads(resultPI.text).get("feeds", [])
            if len(feeds) > 0:
                listReturn.extend({
                    "title": feed["title"],
                    "description": feed["description"],
                    "feed": feed["url"],
                    "originalUrl": feed["originalUrl"],
                    "author": feed["author"],
                    "owner": feed["ownerName"],
                    "language": feed["language"],
                    "generator": feed["generator"],
                    "id_podcastindex": feed["id"],
                    "id_apple": feed["itunesId"],
                    "fetched": int(time.time()),
                    "source": "podcastindex",
                    "cover": feed["image"] if feed["image"] else feed["artwork"],
                    "link": feed["link"],
                    "fromCache": resultPI.from_cache
                } for feed in feeds)
            return listReturn
        else:
            #print(f"Search failed with code: {str(resultPI.status_code)}")
            return []

def jsonify(resultset):
    json_result = dict({"items":[]})
    for i, result in enumerate(resultset):
        json_result["items"].append({
            "uid": result["id_uuid"] if "id_uuid" in result else result["id_apple"],
            "title":  f'{result["title"]} [{result["language"]}]',
            "subtitle": f"{result['feed']}",
            "arg": result["feed"],
            "valid": result["feed"] != "",
            "match": result["title"],
            "type" : "default",
            "mods": {
                "alt": {
                    "valid": True,
                    "arg": result['cover'],
                    "subtitle": f"Copy: {result['cover']}"
                },
                "cmd": {
                    "valid": True,
                    "arg": result['link'],
                    "subtitle": f"Copy: {result['link']}"
                },
                "ctrl": {
                    "valid": True,
                    "arg": result['title'],
                    "subtitle": f"Copy {result['title']}"
                }
            },"text": {
                "copy": f"{result['feed']} (text here to copy)",
                "largetype": f"{result['feed']} (text here for large type)"
            },"quicklookurl": result["link"]
        })
    print(json.dumps(json_result, default=serialize_sets))

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args = " ".join(sys.argv[1:])
    p = Podcasttools(config)
    jsonify(p.searchPodcast(args))