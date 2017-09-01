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
    card = {}
    u = tweet.get('user')
    user ={
        'uid': u.get('id'),
        'name': u.get('name'),
        'allow_all_comment': u.get('allow_all_comment'),
        'follow_me': u.get('follow_me'),
        'bi_followers_count': u.get('bi_followers.count')
    }
    card['user'] = user
    pics = tweet.get('thumbnail_pic')
    if pics:
        card['pics'] = pics
    card['id'] = tweet.get('id')
    card['idstr'] = tweet.get('idstr')
    card['mid'] = tweet.get('mid')
    card['created_at'] = tweet.get('created_at')
    card['htags'] = tc.text_get_hashtag(tweet.get('text')).htags
    card['unames'] = tc.text_get_username(tweet.get('text')).unames
    card['links'] = tc.text_get_link(tweet.get('text')).links
    card['text'] = tc.text_clean(tweet.get('text'),
                                 card['links'],
                                 card['htags'],
                                 card['unames']).cleantext
    card['posseg'] = tc.text_get_pos(card['text'])
    return card
