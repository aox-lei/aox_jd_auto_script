# -*- coding:utf-8 -*-
import logging
from app.utils.base import base


class clock_app(base):
    INDEX_URL = 'https://m.jr.jd.com/spe/qyy/main/index.html?userType=41'
    SIGN_URL = 'https://ms.jr.jd.com/gw/generic/base/h5/m/baseSignInEncrypt'
    TEST_URL = 'https://ms.jr.jd.com/gw/generic/base/h5/m/baseGetMessByGroupType'

    def run(self):
        self.sign()
        pass

    def sign(self):
        payload = {
            'reqData': '{}',
            'sid': self.session.cookies.get('sid'),
            'source': 'jrm'
        }

        r = self.session.post(self.SIGN_URL, data=payload, verify=False)
        as_json = r.json()

        if 'resultData' in as_json:
            result_data = as_json['resultData']
            # statusCode 14 似乎是表示延期到帐的意思, 如: 签到成功，钢镚将于15个工作日内发放到账
            sign_success = result_data['isSuccess'] or result_data['statusCode'] == 14
            message = result_data['showMsg']

            # 参见 daka_app_min.js, 第 1893 行
            continuity_days = result_data['continuityDays']

            if continuity_days > 1:
                message += '; 签到天数: {}'.format(continuity_days)

        else:
            sign_success = False
            message = as_json.get('resultMsg') or as_json.get('resultMessage')

        logging.info('打卡成功: {}; Message: {}'.format(sign_success, message))

        return sign_success

    #
    # def get_sign_data(self):
    #     payload = {
    #         'reqData': '{"clientType":"outH5","userType":41,"groupType":154}',
    #         'sid': self.session.cookies.get('sid'),
    #         'source': 'jrm'
    #     }
    #
    #     sign_data = {}
    #
    #     try:
    #         r = self.session.post(self.test_url, data=payload, verify=False)
    #         as_json = r.json()
    #
    #         if 'resultData' in as_json:
    #             sign_data = r.json()['resultData']['53']
    #
    #         else:
    #             error_msg = as_json.get('resultMsg') or as_json.get(
    #                 'resultMessage')
    #             logging.error('获取打卡数据失败: {}'.format(error_msg))
    #
    #     except Exception as e:
    #         logging.error('获取打卡数据失败: {}'.format(e))
    #
    #     return sign_data
    #
    # def is_signed(self):
    #     sign_data = self.sign_data or self.get_sign_data()
    #
    #     signed = False
    #
    #     try:
    #         signed = sign_data['signInStatus'] == 1
    #         logging.info('今日已打卡: {}'.format(signed))
    #
    #     except Exception as e:
    #         logging.error('返回数据结构可能有变化, 获取打卡数据失败: {}'.format(e))
    #
    #     return signed
