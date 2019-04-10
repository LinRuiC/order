# -*- coding: utf-8 -*-
from application import app
from flask import request,g,jsonify

from common.models.member.Member import Member
from common.libs.member.MemberService import MemberService
import  re

'''
api认证
'''
@app.before_request
def before_request_api():
    api_ignore_urls = app.config['API_IGNORE_URLS']

    path = request.path
    if '/api' not in path:
        return

    member_info = check_member_login()
    g.member_info = None
    if member_info:
        g.member_info = member_info

    pattern = re.compile('%s' % "|".join( api_ignore_urls ))
    if pattern.match(path):
        return

    if not member_info :
        resp = {'code': -1, 'msg': '未登录~', 'data': {}}
        return jsonify(resp)

    return


'''
判断用户是否已经登录
'''
def check_member_login():
    # 获取Authorization: 20bef53d4bd41ef49a561414cb0e6ba8#2
    auth_cookie = request.headers.get("Authorization")

    #auth_cookie为 20bef53d4bd41ef49a561414cb0e6ba8#2
    if auth_cookie is None:
        return False

    # auth_info[1] 就是会员id
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        # 查询会员信息
        member_info = Member.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if member_info is None:
        return False

    if auth_info[0] != MemberService.geneAuthCode( member_info ):
        return False

    # 会员状态 是否有效
    if member_info.status != 1:
        return False

    return member_info