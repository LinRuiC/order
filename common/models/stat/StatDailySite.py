# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, Numeric
from sqlalchemy.schema import FetchedValue
from application import db


class StatDailySite(db.Model):
    # 全站日统计
    __tablename__ = 'stat_daily_site'

    id = db.Column(db.Integer, primary_key=True)
    # 日期
    date = db.Column(db.Date, nullable=False, index=True)
    # 当日应收总金额
    total_pay_money = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    # 会员总数
    total_member_count = db.Column(db.Integer, nullable=False)
    # 当日新增会员数
    total_new_member_count = db.Column(db.Integer, nullable=False)
    # 当日订单数
    total_order_count = db.Column(db.Integer, nullable=False)
    # 分享数
    total_shared_count = db.Column(db.Integer, nullable=False)
    # 最后一次更新时间
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    # 插入时间
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
