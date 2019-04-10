# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from  flask import request,jsonify,g
from application import  app,db
import requests,json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.food.WxShareHistory import WxShareHistory
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService

# 未授权绑定 授权后登录 授权数据保存到数据库 如果已完成绑定，该用户数据存储在数据库的话 不执行此视图函数
@route_api.route("/member/login",methods = [ "GET","POST" ])
def login():
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }
    req = request.values
    # 获取code
    code = req['code'] if 'code' in req else ''
    if not code or len( code ) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    # 获取openid
    openid = MemberService.getWeChatOpenId( code )
    print("openid",openid)

    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    # 获取用户名，性别，头像
    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    '''
        判断是否已经测试过，注册了直接返回一些信息
    '''
    # 从第三方登录绑定关系表获取信息
    bind_info = OauthMemberBind.query.filter_by( openid = openid,type = 1 ).first()
    # 没有信息则进行注册
    if not bind_info:
        # 会员表
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()    # 获取随机随机salt
        model_member.updated_time = model_member.created_time = getCurrentDate() # 获取当前格式化的时间
        # 提交到数据库
        db.session.add(model_member)
        db.session.commit()

        # 第三方登录绑定关系表
        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''
        model_bind.updated_time = model_bind.created_time = getCurrentDate() # 获取当前格式化的时间
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id = bind_info.member_id).first()
    # 生成cookie值 传递给前端 设置好cookie值 下次不用绑定直接登录
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify( resp )


# 已授权绑定 从数据库中获取数据 直接登录
@route_api.route("/member/check-reg",methods = [ "GET","POST" ])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    # req:  CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('code', '0232eG2B159bed0SAE0B1chH2B12eG2V')])])
    req = request.values

    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    # 未从数据库查询到数据 表示未绑定
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)

    # 获取会员信息
    member_info = Member.query.filter_by( id = bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    # 生成cookie值 传递给前端 设置好cookie值 下次不用绑定直接登录
    token = "%s#%s"%( MemberService.geneAuthCode( member_info ),member_info.id )
    resp['data'] = { 'token':token }
    return jsonify(resp)

# 分享功能
@route_api.route("/member/share",methods = [ "POST" ])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    url = req['url'] if 'url' in req else ''
    member_info = g.member_info
    # 微信分享记录表对象
    model_share = WxShareHistory()
    if member_info:
        model_share.member_id = member_info.id
    model_share.share_url = url
    model_share.created_time = getCurrentDate()
    db.session.add(model_share)
    db.session.commit()
    return jsonify(resp)

# 询问是否确定 删除/回复 弹框
@route_api.route("/member/info")
def memberInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    member_info = g.member_info
    resp['data']['info'] = {
        "nickname":member_info.nickname,
        "avatar_url":member_info.avatar
    }
    return jsonify(resp)