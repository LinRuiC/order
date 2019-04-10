# -*- coding: utf-8 -*-
from application import app
from flask import request,g,redirect

from common.models.User import ( User )
from common.libs.user.UserService import ( UserService )
from common.libs.UrlManager import ( UrlManager )
from common.libs.LogService import LogService
import  re

# before_request：在每次请求前运行
@app.before_request
def before_request():
    ignore_urls = app.config['IGNORE_URLS']
    ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
    path = request.path

    # 如果是静态文件路径就不用验证用户是否登录
    pattern = re.compile('%s' % ("|".join(ignore_check_login_urls) ))
    if pattern.match(path):
        return

    if '/api' in path:
        return


    user_info = check_login()
    g.current_user = None
    # 用户已登录
    if user_info:
        g.current_user = user_info

    #加入访问日志到用户访问记录表
    LogService.addAccessLog()
    # 不用验证的路径
    pattern = re.compile('%s' % "|".join(ignore_urls))
    if pattern.match(path):
        return

    if not user_info :
        # 用户未登录 跳转到登录界面
        return redirect( UrlManager.buildUrl( "/user/login" ) )

    return


'''
判断用户是否已经登录
'''
def check_login():
    cookies = request.cookies
    # 假设auth_cookies内容：de0e0f7e2848bcbb9e00fd5458393257#1
    auth_cookie = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None


    if '/api' in request.path:
        app.logger.info(request.path)
        auth_cookie = request.headers.get("Authorization")
        app.logger.info( request.headers.get("Authorization") )

    # cookie为空
    if auth_cookie is None:
        return False

    # de0e0f7e2848bcbb9e00fd5458393257  # 1
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        # 以用户id查找用户信息
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode( user_info ):
        return False

    # 用户状态 1有效 0无效
    if user_info.status != 1:
        return False

    return user_info

