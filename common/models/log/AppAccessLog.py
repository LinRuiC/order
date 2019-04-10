# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from application import  db



class AppAccessLog(db.Model):
    # 用户访问记录表
    __tablename__ = 'app_access_log'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.BigInteger, nullable=False, index=True, server_default=db.FetchedValue())
    # 当前访问的refer
    referer_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    # 访问的url
    target_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    # get和post参数
    query_params = db.Column(db.Text, nullable=False)
    # 访问User-Agent
    ua = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    # 访问ip
    ip = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    # json格式备注字段
    note = db.Column(db.String(1000), nullable=False, server_default=db.FetchedValue())
    # 创建时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
