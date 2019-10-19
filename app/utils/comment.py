# -*- coding:utf-8 -*-
'''
    京东订单自动评价
'''
import json
import logging
import random
import sys
import time
from urllib import parse

import requests
from furl import furl
from requests_html import HTML

from app.utils.base import base


class Comment(base):
    COMMENT_PATH = './data/comment.txt'
    COMMENT_PRODUCT_LIST = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=%d'
    PRODUCT_COMMENT_LIST_URL = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv658&productId=%d&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    comment_list = None
    req_headers = {
        'User-Agen':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer':
        'https://club.jd.com/myJdcomments/orderVoucher.action?ruleid=76988862343',
        'X-Requested-With': 'XMLHttpRequest'
    }
    sort = 0

    def __init__(self):
        super(Comment, self).__init__()
        if self.comment_list is None:
            self.comment_list = self.get_comment_list()

        self.load_cookie()

    def get_product_list(self):
        url = self.COMMENT_PRODUCT_LIST % (int(self.sort))
        try:
            result = self.session.get(url, verify=False)
        except Exception as e:
            logging.exception(e)
            return False

        return self.parse_product_list(result.text)

    def start_comment(self):
        if self.sort == 0:
            comment_type = '订单评价'
        elif self.sort == 1:
            comment_type = '晒单评价'
        elif self.sort == 3:
            comment_type = '追加评价'
        elif self.sort == 4:
            comment_type = '服务评价'
        while 1:
            product_list = self.get_product_list()
            if not product_list:
                logging.info(comment_type + '评价完成')
                return True
            # TODO: 测试代码
            # self.getSkuInstallVoucherByOrderId('102750366961')
            # sys.exit()
            for i in product_list:
                if self.sort == 4:
                    result = self.submit_comment(i.get('order_id'))
                if self.sort == 0:
                    result = self.submit_comment(i.get('order_id'),
                                                 i.get('product_id'))
                if self.sort == 3:
                    result = self.submit_comment(i.get('order_id'),
                                                 i.get('product_id'))

                if result:
                    logging.info('【%s成功】 订单id: %d, 商品id: %d' %
                                 (comment_type, int(i.get('order_id')),
                                  int(i.get('product_id'))))
                else:
                    logging.info('【%s失败】 订单id: %d, 商品id: %d' %
                                 (comment_type, int(i.get('order_id')),
                                  int(i.get('product_id'))))
                time.sleep(5)

    def get_comment_list(self):
        with open(self.COMMENT_PATH, 'r', encoding='UTF-8') as f:
            data = f.read()

        return list(filter(None, data.split("\n")))

    def getProductCommentImgList(self, product_id):
        url = self.PRODUCT_COMMENT_LIST_URL % (int(product_id))
        try:
            result = requests.get(url, verify=False)
        except Exception as e:
            logging.exception(e)
            return False

        data = result.text.replace('fetchJSON_comment98vv658(',
                                   '').replace(');', '')
        images = []
        if data:
            data = json.loads(data)
            for i in data['comments']:
                if i.get('images'):
                    for _images in i.get('images'):
                        images.append(_images.get('imgUrl'))
                if len(images) >= 3:
                    break

        return images


class ServerComment(Comment):
    '''
        服务评价
    '''
    COMMENT_URL = 'https://club.jd.com/myJdcomments/insertRestSurvey.action?voteid=145&ruleid=%d'

    def __init__(self):
        super(ServerComment, self).__init__()
        self.sort = 4

    def parse_product_list(self, html):
        html = HTML(html=html)
        tbody_list = html.find(
            '#main > div.mycomment-bd > div.mycomment-table > table > tbody')
        lists = []
        for _tbody in tbody_list:
            _tbody = HTML(html=_tbody.html)
            product_url = furl(
                _tbody.find(
                    'tr.tr-bd > td:nth-child(1) > div.goods-item > div.p-msg > div > a'
                )[0].attrs['href'])
            order_id = _tbody.find('tr.tr-th > td > span.number > a')[0].text
            lists.append({
                'product_id':
                int(str(product_url.path).strip('/').strip('.html')),
                'order_id':
                order_id
            })
        return lists

    def getSkuInstallVoucherByOrderId(self, order_id):
        url = 'https://club.jd.com/myJdcomments/getSkuInstallVoucherByOrderId.action?callback=jQuery7340659&orderId={}&_={}'.format(
            order_id, time.time())
        result = self.session.get(url,
                                  headers=self.req_headers,
                                  verify=False,
                                  proxies={'https': "http://127.0.0.1:8888"})
        data = result.text.replace('jQuery7340659(', '').replace(');', '')
        data = json.loads(data)
        if data.get('success') is True:
            voucherList = data.get('result').get('voucherList')
            if voucherList:
                saveSkuInstallVoucherByOrderIdUrl = 'https://club.jd.com/myJdcomments/saveSkuInstallComment.action'
                post_data = {
                    'orderId': order_id,
                    'pin': voucherList[0].get('pin'),
                    'associateId': voucherList[0].get('associateId'),
                    'userClient': "2",
                    'score1': '1',
                    'ip': '192.168.1.1',
                    'content': '安装师傅很用心, 很不错, 非常感谢',
                }
                result = self.session.post(
                    saveSkuInstallVoucherByOrderIdUrl,
                    data=post_data,
                    headers=self.req_headers,
                    verify=False,
                    proxies={'https': 'http://127.0.0.1:8888'})
                data = json.loads(result.text)
                if data.get('success') is True:
                    return True
                else:
                    print(data)

    def submit_comment(self, order_id):
        ''' 服务评价 '''
        post_data = {
            'oid': order_id,
            'gid': 69,
            'sid': 549656,
            'tags': '',
            'ro1827': '1827A1',
            'ro1828': '1828A1',
            'ro1829': '1829A1'
        }
        results = self.session.post(self.COMMENT_URL % (int(order_id)),
                                    data=post_data,
                                    headers=self.req_headers,
                                    verify=False)
        return results.text


class ProductComment(Comment):
    COMMENT_URL = 'https://club.jd.com/myJdcomments/saveProductComment.action'

    def __init__(self):
        super(ProductComment, self).__init__()
        self.sort = 0

    def parse_product_list(self, html):
        html = HTML(html=html)
        order_list = html.find(
            '#main > div.mycomment-bd > div.mycomment-table table tbody')

        list = []
        for _order in order_list:
            _product_list = _order.find('tr.tr-bd')
            order_id = _order.find('tr.tr-th > td > span.number > a')[0].text
            for _product in _product_list:
                product_url = furl(
                    _product.find('div.goods-item > div.p-msg > div.p-name > a'
                                  )[0].attrs['href'])

                list.append({
                    'order_id':
                    order_id,
                    'product_id':
                    int(str(product_url.path).strip('/').strip('.html'))
                })
        return list

    def submit_comment(self, order_id, product_id):
        ''' 评价商品 '''
        content = random.sample(self.comment_list, 1)[0]

        comment_tags = self.getProductCommentTag(product_id)

        params = {
            'orderId': order_id,
            'productId': product_id,
            'content': parse.quote(content),
            'imgs': ','.join(self.getProductCommentImgList(product_id)),
            'score': 5,
            'anonymousFlag': 1,
            'saveStatus': 2
        }
        if comment_tags:
            tags = [[str(comment_tags[0]['id']), comment_tags[0]['name']]]
            params['tag'] = parse.quote(json.dumps(
                tags,
                ensure_ascii=False,
            ))

        results = self.session.post(
            'https://club.jd.com/myJdcomments/saveProductComment.action',
            data=params,
            headers=self.req_headers,
            verify=False)
        results = json.loads(results.text)

        if results.get('success') != True:
            logging.warning(results.get('error'))
            del params['imgs']

            results = self.session.post(
                'https://club.jd.com/myJdcomments/saveProductComment.action',
                data=params,
                headers=self.req_headers,
                verify=False)
            results = json.loads(results.text)

        if results.get('success') == True:
            return True
        else:
            logging.warning(results.get('error'))
            return False

    def getProductCommentTag(self, product_id):
        url = 'https://club.jd.com/myJdcomments/getTagCommentsBySkuId.action?callback=jQuery4334469&voucherstatus=0&productId=%d&cateFirst=1320&cateSecond=1585&cateThird=3986&_=%d' % (
            product_id, time.time())

        try:
            result = self.session.get(url,
                                      verify=False,
                                      headers=self.req_headers)
        except Exception as e:
            logging.exception(e)
            return False

        data = result.text.replace('jQuery4334469(', '').replace(');', '')
        data = json.loads(data)
        if data.get('tagRecommend'):
            return data.get('tagRecommend')

        return False


class AppendComment(Comment):
    def __init__(self):
        super(AppendComment, self).__init__()
        self.sort = 3

    def parse_product_list(self, html):
        html = HTML(html=html)
        product_list = html.find(
            '#main > div.mycomment-bd > div.mycomment-table > table > tr > td > div > a'
        )
        list = []
        for _product in product_list:
            _url = furl(_product.attrs['href'])
            list.append({
                'order_id': _url.args['orderId'],
                'product_id': _url.args['sku']
            })

        return list

    def submit_comment(self, order_id, product_id):
        url = 'https://club.jd.com/afterComments/saveAfterCommentAndShowOrder.action'
        content = random.sample(self.comment_list, 1)[0]
        params = {
            'orderId': order_id,
            'productId': product_id,
            'content': parse.quote(content),
            'imgs': ','.join(self.getProductCommentImgList(product_id)),
            'anonymousFlag': 1,
        }

        results = self.session.post(url,
                                    data=params,
                                    headers=self.req_headers,
                                    verify=False)
        results = json.loads(results.text)

        if results.get('success') == True:
            return True
        else:
            logging.warning(results)
            return False
