# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db


class WxShareHistory(db.Model):
    # 微信分享记录
    __tablename__ = 'wx_share_history'

    id = db.Column(db.Integer, primary_key=True)
    # 会员id
    member_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    # 分享的页面url
    share_url = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    # 创建时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
