# 京东自动完成脚本

目前只完成京东订单自动评价, 评价时会自动上传商品图片

## 一、安装
### 1. 程序依赖
1. python3.5 +
2. selenium
3. chrome浏览器

### 2. 安装配置
1. 安装virtualenv 虚拟环境
2. source 加载虚拟环境
3. 安装模块
```
pip install -r requirement.txt
```
4. 配置selenium
自行百度吧

## 二、使用
```
python manage.py comment --username 京东用户名 --password 京东账户密码
```
程序不会记录你的账号密码, 不相信的可以直接看源码
首次登录会自动调用selenium自动输入账号密码, 如果需要验证码, 直接在命令行中输入网页上的验证码回车即可。
程序会自动登录, 登录后生成cookie.txt文件, 下次就不需要再登录了。

## 三、评论内容扩展
可以打开comment.txt文件, 每行一个评论内容, 在评价时会自动随机选取一条进行评价
, 如果有比较好的评论, 希望可以提交给我, 我添加到项目中
