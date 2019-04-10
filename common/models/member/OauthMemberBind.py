# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from application import db


class OauthMemberBind(db.Model):
    # 第三方登录绑定关系表
    __tablename__ = 'oauth_member_bind'
    __table_args__ = (
        db.Index('idx_type_openid', 'type', 'openid'),
    )

    id = db.Column(db.Integer, primary_key=True)
    # 会员id
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 客户端来源类型。qq,weibo,weixin
    client_type = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    # 类型 type 1:wechat
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 第三方id
    openid = db.Column(db.String(80), nullable=False, server_default=db.FetchedValue())
    unionid = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    extra = db.Column(db.Text, nullable=False) #额外字段
    # 最后更 新时间
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    # 插入时 间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
