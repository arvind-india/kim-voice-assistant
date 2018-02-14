# -*- coding: utf-8-*-
import logging
import requests
import json
import random,math

WORDS = ["你是谁", "你是做啥的"]  #  kim的自我介绍
PRIORITY = 0
logger = logging.getLogger()
from utils.aliyun_fc.fc_client import FcClient
from config.profile import city, myname, ali_appcode
from config.path import APP_PATH
from src.plugins import is_all_word_segment_in_text


def handle(text, mic, profile, iot_client=None, chatbot=None):
    """
    处理
    :param text:
    :param mic:
    :param profile:
    :param iot_client:
    :return:
    """
    mic.say('好的，请稍等')
    fc_client = FcClient.get_instance()

    data = {
        'host': 'http://ali-joke.showapi.com',
        'path': '/textJoke',
        'method': 'GET',
        'appcode': ali_appcode,
        'payload': {
            'maxResult': '50',
            'page': '1',
            'time': ''
        },
        'bodys': {},
        'querys': ''
    }
    joke_random = random.randint(0, 9000)
    data['payload']['page'] = math.floor(joke_random/50)
    joke_id_in_page = joke_random % 50
    result_raw = json.loads(fc_client.call_function('aliyun_apimarket', payload=data).data.decode('utf8'))
    logger.info(result_raw)
    if result_raw['showapi_res_code'] == 0:
        joke_content = result_raw['showapi_res_body']['contentlist'][joke_id_in_page]
        mic.say(joke_content['text'].replace('br', ' ').replace('<', '').replace('>', ''))
    else:
        mic.say('我好像出了什么问题，需要治疗一下。调试信息：'+json.dumps(result_raw))


def is_valid(text):
    return is_all_word_segment_in_text(WORDS, text)
