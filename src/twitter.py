#!/usr/bin/env python
# -*- Coding: utf-8 -*-

from datetime import datetime
import re
import requests

def make_token(apikey, apisecret):
    """
    TwitterのAPIKeyとAPISecretからAPIToken(Bearer token)を生成します。APITokenは基本的に変わらないので保存されるべきです。
    """
    endpoint = "https://api.twitter.com/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {"grant_type": "client_credentials"}
    response = requests.post(endpoint, data=payload, headers=headers, auth=(apikey, apisecret))

    if response.ok:
        auth = response.json()
        return auth["access_token"]
    else:
        raise Exception("server returns error")

def egosearch_tweets(access_token, screen_name, regex, previously_fetched_time):
    """
    対象のユーザーから正規表現に当てはまるツイートを抽出します。前回抽出したツイートより古いツイートは抽出されません。
    """
    endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {"screen_name": screen_name}
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(endpoint, params=params, headers=headers)

    if response.ok:
        tl_tweets = response.json()

        tweets = []

        for tweet in tl_tweets:
            tweettime = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
            tweet["unixtime"] = tweettime.strftime("%s")
            if re.match(regex, tweet["text"]) and int(tweet["unixtime"]) > int(previously_fetched_time):
                tweets.append(tweet)

        return sorted(tweets, key=lambda tweet: tweet["unixtime"], reverse=True)
    else:
        raise Exception("server returns error")
