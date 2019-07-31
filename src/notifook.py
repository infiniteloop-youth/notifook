#!/usr/bin/env python
# -*- Coding: utf-8 -*-

from argparse import ArgumentParser
from json import dump, dumps, load
from os import environ
from os.path import abspath, dirname, exists, join
import sys
from requests import post

import twitter
import facebook

DIR = dirname(dirname(abspath(__file__)))

SLACK_TEXT = environ.get("SLACK_TEXT")
SLACK_WEBHOOK = environ.get("SLACK_WEBHOOK")
SLACK_NAME = environ.get("SLACK_NAME")
SLACK_CHANNEL = environ.get("SLACK_CHANNEL")
SLACK_ICON = environ.get("SLACK_ICON")
TWITTER_TEXT = environ.get("TWITTER_TEXT")
TWITTER_TOKEN = environ.get("TWITTER_TOKEN")
TWITTER_SCREENNAME = environ.get("TWITTER_SCREENNAME")
TWITTER_REGEX = environ.get("TWITTER_REGEX")
FACEBOOK_TEXT = environ.get("FACEBOOK_TEXT")
FACEBOOK_TOKEN = environ.get("FACEBOOK_TOKEN")
FACEBOOK_SCREENNAME = environ.get("FACEBOOK_SCREENNAME")
FACEBOOK_REGEX = environ.get("FACEBOOK_REGEX")

def send_message(endpoint, text, channel, username, icon):
    """
    SlackのチャンネルにIncomingWebhookを使用してメッセージを送信します。
    """
    headers = {"Content-Type": "multipart/form-data"}
    payload = {
        "text": text,
        "channel": channel,
        "username": username,
        "icon_emoji": icon
        }
    response = post(endpoint, data=dumps(payload), headers=headers)

    return response.ok


def main():
    """メイン"""

    # 引数をパース
    parser = ArgumentParser(description="The most useful ego-search software")
    parser.add_argument("-d", "--dry", help="Testing mode", action="store_true")
    parser.add_argument("-t", "--twitter_oauth", help="Make Twitter token from APIKey and APISecret", action="store_true")
    parser.add_argument("-f", "--facebook_oauth", help="Make Facebook token from APIKey and APISecret", action="store_true")
    args = parser.parse_args()

    # 各種トークン生成
    if args.twitter_oauth:
        api_key = input("APIKey: ")
        api_secret = input("APISecret: ")
        print("Your access token is ...: "+twitter.make_token(api_key, api_secret))
        sys.exit()

    if args.facebook_oauth:
        api_key = input("APIKey: ")
        api_secret = input("APISecret: ")
        print("Your access token is ...: "+facebook.make_token(api_key, api_secret))
        sys.exit()

    # 前回抽出し投稿時間を読み込み、なければダミーを生成
    previously_fetched_times = {}
    if exists(join(DIR,"previously_fetched_times.json")):
        with open(join(DIR,"previously_fetched_times.json"), "r") as f:
            previously_fetched_times = load(f)
    else:
        previously_fetched_times["twitter"] = 0
        previously_fetched_times["facebook"] = 0

    # Make Egosearch Great Again(https://ja.wikipedia.org/wiki/Make_America_Great_Again)
    tweets = twitter.egosearch_tweets(
        access_token=TWITTER_TOKEN,
        screen_name=TWITTER_SCREENNAME,
        regex=TWITTER_REGEX,
        previously_fetched_time=previously_fetched_times["twitter"]
    )

    # Make Egosearch Great Again(https://ja.wikipedia.org/wiki/Make_America_Great_Again)
    posts = facebook.egosearch_posts(
        access_token=FACEBOOK_TOKEN,
        screen_name=FACEBOOK_SCREENNAME,
        regex=FACEBOOK_REGEX,
        previously_fetched_time=previously_fetched_times["facebook"]
    )

    # 投稿データ生成
    postdata = SLACK_TEXT+"\n"

    newpost = False

    if tweets:
        newpost = True
        postdata += TWITTER_TEXT+"\n"
        for tweet in tweets:
            postdata += "https://twitter.com/{}/status/{}\n".format(tweet['user']['screen_name'], tweet["id_str"])

        previously_fetched_times["twitter"] = tweets[0]["unixtime"]

    if posts:
        newpost = True
        postdata += FACEBOOK_TEXT+"\n"
        for post in posts:
            postdata += post["permalink_url"]+"\n"

        previously_fetched_times["facebook"] = posts[0]["unixtime"]

    # 投稿開始!
    if newpost is True:
        if args.dry:
            print("{}|{} {}\n{}".format(
                SLACK_CHANNEL,
                SLACK_ICON,
                SLACK_NAME,
                postdata
            ))
        else:
            send_message(
                endpoint=SLACK_WEBHOOK,
                text=postdata,
                channel=SLACK_CHANNEL,
                username=SLACK_NAME,
                icon=SLACK_ICON
            )
    else:
        print("No new posts")

    # データを保存
    with open(join(DIR,"previously_fetched_times.json"), "w") as f:
        dump(previously_fetched_times, f)

if __name__ == '__main__':
    main()
