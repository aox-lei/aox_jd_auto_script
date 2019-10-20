# -*- coding:utf-8 -*-
import requests
import logging
import click
from app.utils.base import Login
from app.utils.comment import ServerComment, ProductComment, AppendComment
from app.utils.bean_app import bean_app as bean_app_shell
from app.utils.bean_vip import bean_vip as bean_vip_shell
from app.utils.clock_app import clock_app as clock_app_shell
from app.utils.clock import clock as clock_shell
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a',
    filename='data/jd.log')

logger = logging.getLogger()

console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


@click.group()
def cli():
    pass


@click.command()
def comment():
    login_result = Login().login()
    if login_result:
        logging.info('登录成功')

    # 服务评价
    ServerComment().start_comment()
    # 商品评价
    # ProductComment().start_comment()
    # 追加评价
    # AppendComment().start_comment()


@click.command()
def bean_app():
    login_result = Login().login()
    if login_result:
        logging.info('登录成功')

    bean_app_shell().run()


@click.command()
def bean_vip():
    login_result = Login().login()
    if login_result:
        logging.info('登录成功')

    bean_vip_shell().run()


@click.command()
def clock_app():
    login_result = Login().login()
    if login_result:
        logging.info('登录成功')

    clock_app_shell().run()


@click.command()
def clock():
    login_result = Login().login()
    if login_result:
        logging.info('登录成功')

    clock_shell().run()


cli.add_command(comment)
cli.add_command(bean_app)
cli.add_command(bean_vip)
cli.add_command(clock_app)
cli.add_command(clock)
if __name__ == '__main__':
    cli()
