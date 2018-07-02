# -*- coding:utf-8 -*-
'''
    京东APP签到领京豆
'''
import logging
import json
import random
from app.utils.base import base


class bean_app(base):
    INFO_URL = 'https://api.m.jd.com/client.action?functionId=queryBeanIndex'
    SIGN_URL = 'https://api.m.jd.com/client.action?functionId=signBeanStart'

    client_info = {'client': 'ld', 'clientVersion': '1.0.0'}

    def run(self):
        self.sign()
        try:
            data = self.fetch_data(self.INFO_URL)
        except Exception as e:
            logging.exception(e)
            return False

        # 根据测试, 2 表示已签到, 4 表示未签到, 5 表示未登录
        signed = (data['status'] == '2')
        sign_days = int(data['continuousDays'])
        beans_count = int(data['totalUserBean'])

        logging.info('今日已签到: {}; 签到天数: {}; 现有京豆: {}'.format(
            signed, sign_days, beans_count))
        return signed

    def sign(self):
        try:
            data = self.fetch_data(self.SIGN_URL)
        except Exception as e:
            logging.exception(e)
            return False

        sign_success = (data['status'] == '1')
        message = data['signShowBean']['signText']
        message = message.replace('signAward',
                                  data['signShowBean']['signAward'])
        logging.info('签到成功: {}; Message: {}'.format(sign_success, message))

        if 'awardList' in data['signShowBean']:
            # "complated": 原文如此, 服务端的拼写错误...
            poker_picked = data['signShowBean']['complated']

            if not poker_picked:
                pick_success = self.pick_poker(data['signShowBean'])
                # 同时成功才视为签到成功
                sign_success &= pick_success

        return sign_success

    def pick_poker(self, poker):
        poker_to_pick = random.randint(1, len(poker['awardList']))

        try:
            payload = {'body': json.dumps({'index': poker_to_pick})}
            data = self.fetch_data(self.poker_url, payload=payload)
        except Exception as e:
            logging.exception(e)
            return False

        message = data['signText'].replace('signAward', data['signAward'])
        self.logger.info('翻牌成功: {}'.format(message))
        return True

    def fetch_data(self, url, payload=None):
        if payload is not None:
            payload = dict(payload.items() + self.client_info.items())
        else:
            payload = self.client_info

        r = self.session.get(url, params=payload, verify=False)

        try:
            as_json = r.json()
        except Exception:
            logging.exception()

        if as_json['code'] != '0' or 'errorCode' in as_json or 'errorMessage' in as_json:
            error_msg = as_json.get('echo') or as_json.get(
                'errorMessage') or str(as_json)
            error_code = as_json.get('errorCode') or as_json.get('code')
            logging.error('error_msg: %s, error_code: %d' % (error_msg,
                                                             int(error_code)))
            return False
        # 请求成功
        return as_json['data']
