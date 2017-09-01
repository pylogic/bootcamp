# -*- coding:utf-8 -*-
# ganben
# subtract @? # and links, get clean data.
# input text -- tuple

import jieba.posseg as pseg
import jieba.analyse
import re
from collections import namedtuple


# re patterns for @ ## link etc.
uname_re = re.compile('\@(.+?)\s')
hashtag_re = re.compile('\#(.+?)\#')
link_re = re.compile('http://(.+?)\s')
endp_re = re.compile('\u200b\Z')
repl_htag_re = re.compile('#')
repl_uname_re = re.compile('@')

# jieba pos cut with configurable dicts
jieba.initialize()    #pre load
#TODO add a main dict location


# get uid
def text_get_username(text):
    """
    :param text:
    :return: namedtuple( text, unames [])
    """
    result = namedtuple('Tnames', ['text', 'unames'], verbose=True)
    result.text = text
    try:
        result.unames = uname_re.findall(text)
    except Exception as e:
        result.unames = []

    return result

# get hash tags
def text_get_hashtag(text):
    """
    re get hastag list
    :param text:
    :return: result = namedtuple text str, hashtags[]
    """
    result = namedtuple('Thtags', ['text', 'htags'], verbose=True)
    result.text = text
    try:
        result.htags = hashtag_re.findall(text)
    except Exception as e:
        result.htags = []

    return result

# get links (any kind)
def text_get_link(text):
    """
    re get link list
    :param text:
    :return: result namedtuple text str, links []
    """
    result = namedtuple('Tlinks', ['text', 'links'], verbose=True)
    result.text = text
    try:
        result.links = link_re.findall(text)
    except Exception as e:
        result.links = []
    return result

# return a cleaned text tuple
def text_clean(text, tlinks, thtags, tnames):
    """
    replace links @ with \s, replace # with "
    :param text:
    :param tlinks: namedtuple
    :param thtags: namedtuple
    :param tnames: namedtuple
    :return: namedtuple cleantext, links[], htags[], unames[]
    """
    cleantext = link_re.sub(' ', text)
    cleantext = repl_htag_re.sub('"', cleantext)
    cleantext = repl_uname_re.sub('他', cleantext) # TODO find a better rplc for name
    ctext = namedtuple('Ctxt', ['cleantext', 'links', 'htags', 'unames'], verbose=True)
    ctext.cleantext = cleantext
    ctext.links = tlinks.links
    ctext.htags = thtags.htags
    ctext.unames = tnames.unames

    return ctext

# get word pos cut
def text_get_pos(cleantext):
    """
    try pos cut, remove @ # link, add @ to dictionary
    jieba must pre-load for a faster
    :param text: text tuple with clean text and named entities
    :return: structured text dict
    """
    seg_list = jieba.cut(cleantext.cleantext)
    # res = {'text': cleantext.cleantext,
    #        'seg_list': seg_list,
    #        'links': cleantext.links,
    #        'htags': cleantext.htags,
    #        'unames': cleantext.unames
    #        }
    return seg_list







