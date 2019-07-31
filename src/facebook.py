#!/usr/bin/env python
# -*- Coding: utf-8 -*-

from datetime import datetime
import re
import requests

def make_token(apikey, apisecret):
    """
    FacebookのAPIKeyとAPISecretからAPIToken(Bearer token)を生成します。APITokenは基本的に変わらないので保存されるべきです。
    """
    endpoint = "https://graph.facebook.com/oauth/access_token"
    params = {
        "grant_type": "client_credentials",
        "client_id": apikey,
        "client_secret": apisecret
    }

    response = requests.post(endpoint, params=params)

    if response.ok:
        auth = response.json()
        return auth["access_token"]
    else:
        raise Exception("server returns error")

def egosearch_posts(access_token, screen_name, regex, previously_fetched_time):
    """
    対象のユーザーから正規表現に当てはまる投稿を抽出します。前回抽出したツイートより古い投稿は抽出されません。
    """
    endpoint = "https://graph.facebook.com/v2.11/"+screen_name+"/feed"
    params = {
        "fields": "created_time,message,id,permalink_url",
        "access_token": access_token
    }
    response = requests.get(endpoint, params=params)

    if response.ok:
        tl_posts = response.json()

        posts = []

        for post in tl_posts["data"]:
            posttime = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S%z")
            post["unixtime"] = posttime.strftime("%s")
            if "message" in post:
                if re.match(regex, post["message"]) and int(post["unixtime"]) > int(previously_fetched_time):
                    posts.append(post)

        return sorted(posts, key=lambda post: post["unixtime"], reverse=True)
    else:
        raise Exception("server returns error")
