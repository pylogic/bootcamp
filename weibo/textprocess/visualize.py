#!/usr/bin/python3
# -*- coding:utf-8 -*-
# ganben
# process raw text to structured data for storage,
# solved problems: 1. if chinese char or non chinese char
# 2. if simplified chinese or traditional chinese and replace
import textprocess.textclean as tc

# used by front
def statuses_to_data(statuses):
    """
    list to raw text, text clean, text cutting, data generation
    :param statuses: list of weibo status
    :return: data for index
    """
    data = {}
    data['total'] = len(statuses)
    cards = []
    for item in statuses:
        card = clean_tweet(item)
        if item.get('retweeted_status'):
            sub_card = clean_tweet(item.get('retweeted_status'))
            card['sub_card'] = sub_card
        cards.append(card)
    return data

# for single tweet
def clean_tweet(tweet):
    """
    process text, user, time, id
    :param tweet: a weibo api returned tweet
    :return:
    """

