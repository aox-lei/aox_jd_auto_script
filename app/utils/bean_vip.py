# -*- coding:utf-8 -*-
'''
    京东会员页面签到领京豆
'''
import re
import logging
import requests
from requests_html import HTML
from app.utils.base import base


class bean_vip(base):
    INFO_URL = 'https://vip.jd.com/member/getUserInfo.html'
    SIGN_URL = 'https://vip.jd.com/common/signin.html'
    INDEX_URL = 'https://vip.jd.com'
    page_data = ''

    def run(self):
        self.sign()
        page_data = self._get_page_data()
        signed = '已签到' in HTML(html=page_data).find('.sign-in')[0].text

        detail = self.session.get(self.INFO_URL, verify=False).json()

        if detail['success']:
            user_info = detail['result']['userInfo']
            beans_count = user_info['userJingBeanNum']
            logging.info('今日已签到: {}; 现在有 {} 个京豆.'.format(signed, beans_count))

        else:
            logging.info('今日已签到: {}'.format(signed))

        return signed

    def sign(self):
        token = self._get_token()
        if not token:
            return False
        payload = {'token': token}

        response = self.session.get(self.SIGN_URL, params=payload, verify=False)
        if response['success']:
            # 签到成功, 获得若干个京豆
            beans_get = response['result'].get('jdnum')
            message = '签到成功, 获得 {} 个京豆.'.format(
                beans_get) if beans_get else '签到成功.'
            logging.info(message)
            return True
        else:
            message = response['resultTips']
            logging.error('签到失败: {}'.format(message))
            return False

    def _get_token(self):
        html = self._get_page_data()
        pattern = r'token:\s*"(\d+)"'

        token = re.search(pattern, html)

        if token:
            token = token.group(1)

        if not token:
            logging.error('token 未找到.')
            return False
        return token

    def _get_page_data(self):
        if not self.page_data:
            try:
                self.page_data = self.session.get(
                    self.INDEX_URL, verify=False).text
            except Exception as e:
                logging.exception(e)
        return self.page_data
