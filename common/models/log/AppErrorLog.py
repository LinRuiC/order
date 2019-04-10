# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from application import  db


class AppErrorLog(db.Model):
    # app错误日志表
    __tablename__ = 'app_error_log'

    id = db.Column(db.Integer, primary_key=True)
    # 当前访问的refer
    referer_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    # 访问的url
    target_url = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue())
    # get和post参数
    query_params = db.Column(db.Text, nullable=False)
    # 日志内容
    content = db.Column(db.String, nullable=False)
    # 插入时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
