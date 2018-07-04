# -*- coding:utf-8 -*-
import logging
from app.utils.base import base


class clock(base):
    INDEX_URL = 'https://bk.jd.com/m/channel/login/daka.html'
    LOGIN_URL = 'https://home.m.jd.com'
    SIGN_URL = 'https://bk.jd.com/m/channel/login/clock.html'
    TEST_URL = INDEX_URL
    JOB_GD_URL = 'https://bk.jd.com/m/channel/login/recDakaGb.html'

    def run(self):
        self.sign()

    def sign(self):
        try:
            data = self.fetch_data(self.SIGN_URL)
            logging.info('打卡成功: ' + data['resultMessage'])
            return True
        except Exception as e:
            if e.code == '0003':
                # 已打卡 7 次, 需要先去 "任务" 里完成一个领钢镚任务...
                logging.info('已打卡 7 次, 去完成领钢镚任务...')
                pick_success = self.pick_gb()

                if pick_success:
                    # 钢镚领取成功, 重新开始打卡任务
                    return self.sign()
                else:
                    e.message = '钢镚领取任务未成功完成.'

            logging.error('打卡失败: ' + e.message)
            return False

    def pick_gb(self):
        # 任务列表在 https://bk.jd.com/m/money/doJobMoney.html 中看
        # 领钢镚的任务的 id 是 82
        try:
            data = self.fetch_data(self.JOB_GD_URL)
            self.logger.info('钢镚领取成功: {}'.format(data['resultMessage']))
            return True

        except Exception as e:
            self.logger.error('领钢镚 -> 钢镚领取失败: {}'.format(e.message))
            return False

    def fetch_data(self, url, payload=None):
        r = self.session.get(url, params=payload)
        try:
            as_json = r.json()
        except ValueError:
            raise Exception(
                'unexpected response: url: {}; http code: {}'.format(
                    url, r.status_code),
                response=r)

        if as_json['success']:
            # 请求成功
            return as_json

        else:
            error_msg = as_json.get('resultMessage') or str(as_json)
            error_code = as_json.get('resultCode')
            raise Exception(error_msg, error_code)
