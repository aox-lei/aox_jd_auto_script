# -*- coding:utf-8 -*-
import requests
import logging
import click
import sys
from jd import Login, ServerComment, ProductComment, AppendComment
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@click.group()
def cli():
    pass


@click.command()
@click.option('--username', required=True)
@click.option('--password', required=True, hide_input=True, prompt=True)
def comment(username, password):
    login_result = Login().login(username, password)
    if login_result:
        logging.info('登录成功')

    # 服务评价
    ServerComment().start_comment()
    # 商品评价
    ProductComment().start_comment()
    # 追加评价
    AppendComment().start_comment()


cli.add_command(comment)

if __name__ == '__main__':
    cli()
